from typing import Dict, List, Tuple
import psycopg2
from .Layer import *
from .Geometry import *
from osgeo import ogr
import os
import threading
import time

"""
矢量数据的属性字段，支持varchar，
"""

attr_type_dict={
    'str':'varchar(100)',
    'int':'int',
    'float':'float'
}

db_attr_dict={
    'outline_color': 'varchar(20)',
    'outline_style': 'int',
    'outline_width': 'float',
    'label_color' :'varchar(20)',
    'nothing':'int',
    'visible' :'int',
    'bind_attr': 'varchar(100)',
    'h_bias': 'int',
    'v_bias': 'int',
    'font_size': 'int',
    'font_color': "varchar(20)",
}

class DBM:
    def __init__(self):
        self.conn=None
        self.sql_record=''
        self.closed = False
        thread_connect=threading.Thread(target=self._connect)
        thread_connect.start()
        time.sleep(1)
        # self._connect()

    def _connect(self):
        while not self.closed:
            if self.conn is None:
                try:
                    self.conn=psycopg2.connect(database="minigis",user="minigiser",password="minigis",host="47.104.149.94",port="5432")
                    self.cur=self.conn.cursor()
                    if self.sql_record!='':
                        self.cur.execute(self.sql_record)
                        self.conn.commit()
                        self.sql_record=''
                except:
                    pass
            else:
                try:
                    self.cur.execute('select 1;')
                    time.sleep(5)
                except:
                    self.conn=None

    
    def get_layers_list(self)->List:
        """
        @description : 获取数据库存储图层名称列表
        @param : None
        @returns : name字符串列表
        """
        
        sql=f"""
            select f_table_name from geometry_columns;
        """
        if self.conn:
            self.cur.execute(sql)
            layer_list= self.cur.fetchall()
            return [ln[0] for ln in layer_list]
        else:
            return []
            

    def get_layers_info(self)->Tuple:
        """
        @description : 获取数据库存储图层（name : str，srid : int，type : str）
        @param :  无
        @returns : 由各个图层信息构成的元组
        """ 
        
        sql=f"""
            select f_table_name,srid,type from geometry_columns;
        """
        if self.conn:
            self.cur.execute(sql)
            layer_info_list=self.cur.fetchall()
            return layer_info_list
        else:
            return []

    def add_layer_from_memory(self,layer:Layer)->None:
        layer_list=self.get_layers_list()
        if layer_list:
            if layer.name in layer_list:
                self.cur.execute(f"drop table {layer.name};")
        trans_dict={
            PointD:'POINT',
            Polyline:'LINESTRING',
            Polygon:'POLYGON',
            MultiPolygon:'MULTIPOLYGON',
            MultiPolyline:'MULTILINESTRING',
            }
        layer_type=trans_dict[layer.type]
        self.create_table(layer.name, layer_type, layer.srid, layer.attr_desp_dict)
        for geometry in layer.geometries:
            self.insert_geometry(layer, geometry)

    def add_layer_from_shp(self, path) -> None:
        os.system(
            'ogr2ogr ' + '-overwrite ' + '-f ' + '"' +
            "PostgreSQL" + '"' + ' PG:' + '"' +
            "host=47.104.149.94 user=minigiser dbname=minigis password=minigis" + '"'
            + ' ' + '"' + path + '"')

    def create_table(self,tablename:str,geom_type:str,srid:int,attr_desp_dict:dict)->None:
        sql_table_attr_list=['gid serial primary key',f'geom Geometry({geom_type},{srid})']\
            +[f'{attr_name} {attr_type}' for attr_name,attr_type in db_attr_dict.items()]\
            +[f'{attr_name} {attr_type_dict[attr_type]}' for attr_name,attr_type in attr_desp_dict.items()]
        sql=f"""
            create table {tablename}(
                {','.join(sql_table_attr_list)}
            );
        """
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql

    def insert_geometry(self,layer:Layer,geomtry:Geometry,create=True)->None:
        if not create and not layer.saved_in_dbm:
            return
        wkt=geomtry.ToWkt()
        attr_name_lst=['geom']+list(db_attr_dict.keys())+list(layer.attr_desp_dict.keys())
        attr_str_lst=[f'st_geometryfromtext(\'{wkt}\',{layer.srid})']
        # if len(geomtry.StyleList)==0:
        #     geomtry.StyleList=[0]*15
        for style_attr in geomtry.StyleList[:len(db_attr_dict)]:
            if type(style_attr)==str:
                attr_str_lst.append(f'\'{style_attr}\'')
            else:
                attr_str_lst.append(str(style_attr))
        for attr in layer.get_attr(geomtry.ID):
            if type(attr)==str:
                attr_str_lst.append(f'\'{attr}\'')
            else:
                attr_str_lst.append(str(attr))
        sql=f"""
            insert into {layer.name}
            ({','.join(attr_name_lst)})
            values({','.join(attr_str_lst)});
        """
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql

    def delete_geometry(self,layer:Layer,geometry_id):
        if not layer.saved_in_dbm:
            return
        gid = None
        for geo in layer.geometries:
            if geo.ID == geometry_id:
                gid = geo.gid
                break
        if gid is not None:
            sql=f"delete from {layer.name} where gid={gid};"
            if self.conn:
                self.cur.execute(sql)
                self.conn.commit()
            else:
                self.sql_record+=sql

    def update_geometry(self,layer:Layer,geomery_id,info_dict:Dict):
        if not layer.saved_in_dbm:
            return
        for k,v in info_dict.items():
            if k=='geom':
                info_dict[k]=f'st_geometryfromtext(\'{v}\',{layer.srid})'
            elif type(v)==str:
                info_dict[k]=f'\'{v}\''

        sql=f"""
            update {layer.name} set {','.join([f'{k}={v}' for k,v in info_dict.items()])}
            where gid={geomery_id};
        """
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql
    
    def update_style(self,layer:Layer,geometry_id,style_list):
        if not layer.saved_in_dbm:
            return
        style_dict=dict(zip(db_attr_dict.keys(),style_list))
        self.update_geometry(layer,geometry_id,style_dict)

    def add_column(self,layer:Layer,attr_name:str,attr_type:str):
        if not layer.saved_in_dbm:
            return
        sql=f"alter table {layer.name} add {attr_name} {attr_type_dict[attr_type]} null;"
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql

    def delete_column(self,layer:Layer,attr_name:str):
        if not layer.saved_in_dbm:
            return
        sql=f"alter table {layer.name} drop {attr_name};"
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql

    
    def modify_column(self,layer:Layer,attr_name:str,new_name):
        if not layer.saved_in_dbm:
            return
        # if new_type:
        #     sql=f"alter table {layer.name} modify {attr_name} {new_type};"
        #     self.cur.execute(sql)
        sql=f"alter table {layer.name} rename column {attr_name} to {new_name};"
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql

    def load_layer(self,layer_name)->Layer:
        assert self.conn is not None
        self.cur.execute(f"select f_geometry_column,srid,type from geometry_columns where f_table_name=\'{layer_name}\';")
        slct_rslt=self.cur.fetchone()
        col_name,layer_srid,layer_type=slct_rslt
        # col_name,layer_srid,layer_type=('geom',3857,'LINESTRING')
        if layer_type=='POINT':
            layer_type_class=PointD
        elif layer_type=='LINESTRING':
            layer_type_class=Polyline
        elif layer_type=='POLYGON':
            layer_type_class=Polygon
        elif layer_type=='MULTILINESTRING':
            layer_type_class=MultiPolyline
        elif layer_type=='MULTIPOLYGON':
            layer_type_class=MultiPolygon
        else:
            layer_type_class=PointD
        cur_layer=Layer(layer_type_class,layer_name,layer_srid)
        #获取属性字段元数据
        self.cur.execute(f"""
            select ordinal_position as Colorder,column_name as ColumnName,data_type as TypeName,
            coalesce(character_maximum_length,numeric_precision,-1) as Length
            from information_schema.columns
            left join (
            select pg_attr.attname as colname,pg_constraint.conname as pk_name from pg_constraint
            inner join pg_class on pg_constraint.conrelid = pg_class.oid
            inner join pg_attribute pg_attr on pg_attr.attrelid = pg_class.oid and pg_attr.attnum = pg_constraint.conkey[1]
            inner join pg_type on pg_type.oid = pg_attr.atttypid
            where pg_class.relname = '{layer_name}' and pg_constraint.contype='p'
            ) b on b.colname = information_schema.columns.column_name
            left join (
            select attname,description as DeText from pg_class
            left join pg_attribute pg_attr on pg_attr.attrelid= pg_class.oid
            left join pg_description pg_desc on pg_desc.objoid = pg_attr.attrelid and pg_desc.objsubid=pg_attr.attnum
            where pg_attr.attnum>0 and pg_attr.attrelid=pg_class.oid and pg_class.relname='{layer_name}'
            )c on c.attname = information_schema.columns.column_name
            where table_schema='public' and table_name='{layer_name}' order by ordinal_position asc
        """)
        slct_rslt=self.cur.fetchall()
        attr_infos=slct_rslt[2+len(db_attr_dict):]
        tradict={'integer':'int','character varying':'str','double precision':'float'}
        for attr_info in attr_infos[1:]:
            cur_layer.add_attr(attr_info[1],tradict[attr_info[2]])
        #set layer attr
        # self.cur.execute(f"select * from {layer_name};")#geometry转为其他类型
        # geoms=self.cur.fetchall()
        #根据不同数据类型读取几何信息，addgeomtry
        if layer_type=='POINT':
            self.cur.execute(f"select st_x({col_name}),st_y({col_name}),* from {layer_name};")
            points =self.cur.fetchall()
            for p in points:
                cur_p=PointD(p[0],p[1],id=p[2])
                for i in range(len(db_attr_dict)):
                    cur_p.StyleList[i]=p[4+i]
                cur_layer.AddGeometry(cur_p,dict(zip([attr[1] for attr in attr_infos],p[4+len(db_attr_dict):])))
        elif layer_type=='LINESTRING':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            lines=self.cur.fetchall()
            for l in lines:
                cur_l=Polyline(l[0],id=l[1])
                for i in range(len(db_attr_dict)):
                    cur_l.StyleList[i]=l[3+i]
                cur_layer.AddGeometry(cur_l,dict(zip([attr[1] for attr in attr_infos],l[3+len(db_attr_dict):])))
        elif layer_type=='POLYGON':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            polygons=self.cur.fetchall()
            for pg in polygons:
                cur_pg=Polygon(pg[0],id=pg[1])
                for i in range(len(db_attr_dict)):
                    cur_pg.StyleList[i]=pg[3+i]
                cur_layer.AddGeometry(cur_pg,dict(zip([attr[1] for attr in attr_infos],pg[3+len(db_attr_dict):])))

        elif layer_type=='MULTIPOLYGON':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            mpolygons=self.cur.fetchall()
            for mpg in mpolygons:
                cur_mpg=MultiPolygon(mpg[0],id=mpg[1])
                for i in range(len(db_attr_dict)):
                    cur_mpg.StyleList[i]=mpg[3+i]
                cur_layer.AddGeometry(cur_mpg,dict(zip([attr[1] for attr in attr_infos],mpg[3+len(db_attr_dict):])))
        elif layer_type=='MULTILINESTRING':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            mlines=self.cur.fetchall()
            for ml in mlines:
                cur_ml=MultiPolyline(ml[0],id=ml[1])
                for i in range(len(db_attr_dict)):
                    cur_ml.StyleList[i]=ml[3+i]
                cur_layer.AddGeometry(cur_ml,dict(zip([attr[1] for attr in attr_infos],ml[3+len(db_attr_dict):])))
        else:
            pass
        cur_layer.saved_in_dbm=True
        return cur_layer


    def delete_layer(self,layer_name):
        self.drop_table(layer_name)

    def drop_table(self,table_name):
        sql=f"""
            drop table {table_name};
        """
        if self.conn:
            self.cur.execute(sql)
            self.conn.commit()
        else:
            self.sql_record+=sql
    # def execute(self,sql_str):
    #     self.cur.execute(sql_str)

    # def commit(self):
    #     self.cur.commit()

    def test(self):
        # self.create_table('test','POINT',3857)
        # self.conn.commit()
        # self.cur.execute("""
        #     insert into test values(2,st_geometryfromtext(\'POINT(1 1)\',3857));
        # """)
        # self.conn.commit()
        layer_name='lines'
        self.cur.execute(f"""
            select ordinal_position as Colorder,column_name as ColumnName,data_type as TypeName,
            coalesce(character_maximum_length,numeric_precision,-1) as Length
            from information_schema.columns
            left join (
            select pg_attr.attname as colname,pg_constraint.conname as pk_name from pg_constraint
            inner join pg_class on pg_constraint.conrelid = pg_class.oid
            inner join pg_attribute pg_attr on pg_attr.attrelid = pg_class.oid and pg_attr.attnum = pg_constraint.conkey[1]
            inner join pg_type on pg_type.oid = pg_attr.atttypid
            where pg_class.relname = '{layer_name}' and pg_constraint.contype='p'
            ) b on b.colname = information_schema.columns.column_name
            left join (
            select attname,description as DeText from pg_class
            left join pg_attribute pg_attr on pg_attr.attrelid= pg_class.oid
            left join pg_description pg_desc on pg_desc.objoid = pg_attr.attrelid and pg_desc.objsubid=pg_attr.attnum
            where pg_attr.attnum>0 and pg_attr.attrelid=pg_class.oid and pg_class.relname='{layer_name}'
            )c on c.attname = information_schema.columns.column_name
            where table_schema='public' and table_name='{layer_name}' order by ordinal_position asc
        """)
        slct_rslt=self.cur.fetchall()
        return slct_rslt


if __name__=="__main__":
    dbm=DBM()
    print(dbm.test())
    # print(dbm.get_layers_list())