from typing import List, Tuple
import psycopg2
from .Layer import *
from .Geometry import *
from osgeo import ogr

"""
矢量数据的属性字段，支持varchar，
"""

class DBM:
    def __init__(self):
        self._connect()

    def _connect(self):
        self.conn=psycopg2.connect(database="minigis",user="minigiser",password="minigis",host="47.104.149.94",port="5432")
        self.cur=self.conn.cursor()

    
    def get_layers_list(self)->List:
        """
        @description : 获取数据库存储图层名称列表
        @param : None
        @returns : name字符串列表
        """
        
        sql=f"""
            select f_table_name from geometry_columns;
        """
        self.cur.execute(sql)
        layer_list= self.cur.fetchall()
        return [ln[0] for ln in layer_list]

    def get_layers_info(self)->Tuple:
        """
        @description : 获取数据库存储图层（name : str，srid : int，type : str）
        @param :  无
        @returns : 由各个图层信息构成的元组
        """
        
        sql=f"""
            select f_table_name,srid,type from geometry_columns;
        """
        self.cur.execute(sql)
        layer_info_list=self.cur.fetchall()
        return layer_info_list

    def add_layer_from_memory(self,layer:Layer)->None:
        if layer.name in self.get_layers_list():
            self.cur.execute(f"drop table {layer.name}")
        if layer.type==PointD:
            layer_type='POINT'
        elif layer.type==Polyline:
            layer_type='LINESTRING'
        elif layer.type==Polygon:
            layer_type='Polygon'
        elif layer.type==MultiPolyline:
            layer_type='MULTILINESTRING'
        elif layer.type==MultiPolygon:
            layer_type='MULTIPOLYGON'
        else:
            layer_type='POINT'
        self.create_table(layer.name,layer_type,layer.srid,layer.attr_desp_dict)
        for geometry in layer.geometries:
            self.insert_geometry(layer,geometry)
        self.conn.commit()

    def add_layer_from_shp(self, path)->None:
        driver = ogr.GetDriverByName('ESRI Shapefile')
        data_source = driver.Open(path, 0)
        layer_name = path.split('/')[-1].split('.')[0]
        assert data_source is not None
        ori_layer = data_source.GetLayer(0)
        wkt_list = list()
        feat = ori_layer.GetNextFeature()
        while feat:
            wkt_list.append(feat.geometry().ExportToWkt())
        geom_type_dict = {
            ogr.wkbPoint : PointD,
            ogr.wkbLineString : Polyline,
            ogr.wkbPolygon : Polygon,
            ogr.wkbMultiLineString : MultiPolyline,
            ogr.wkbMultiPolygon : MultiPolygon
        }
        sql = f"""
                    create table {layer_name}(
                        gid int primary key,
                        geom Geometry({None},{3857})
                        {''.join([f',{attr_name} {attr_type}' for attr_name, attr_type in attr_desp_dict.items()])}
                    );
                """
        self.cur.execute(sql)#yaogai!

    def create_table(self,tablename,geom_type,srid,attr_desp_dict)->None:
        sql=f"""
            create table {tablename}(
                gid int primary key,
                geom Geometry({geom_type},{srid})
                {''.join([f',{attr_name} {attr_type}' for attr_name,attr_type in attr_desp_dict.items()])}
            );
        """
        self.cur.execute(sql)

    def insert_geometry(self,layer:Layer,geomtry:Geometry)->None:
        wkt=geomtry.ToWkt()
        sql=f"""
            insert into {layer.name}(gid,geom{''.join([f',{k}' for k in layer.attr_desp_dict.keys()])})
            values({geomtry.ID},st_geometryfromtext(\'{wkt}\',{layer.srid}){''.join([f',{attr}' for attr in  layer.get_attr(geomtry.ID)])});
        """
        self.cur.execute(sql)

    def load_layer(self,layer_name)->Layer:
        self.cur.execute(f"select f_geometry_column,srid,type from geometry_columns where f_table_name=\'{layer_name}\';")
        slct_rslt=self.cur.fetchall()
        col_name,layer_srid,layer_type=slct_rslt[0]
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
        attr_info=slct_rslt[3:]
        #set layer attr
        # self.cur.execute(f"select * from {layer_name};")#geometry转为其他类型
        # geoms=self.cur.fetchall()
        #根据不同数据类型读取几何信息，addgeomtry
        if layer_type=='POINT':
            self.cur.execute(f"select st_x({col_name}),st_y({col_name}),* from {layer_name};")
            points =self.cur.fetchall()
            for p in points:
                cur_p=PointD(p[0],p[1],p[2])
                cur_layer.AddGeometry(cur_p,dict(zip([attr[0] for attr in attr_info],p[4:])))
        elif layer_type=='LINESTRING':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            lines=self.cur.fetchall()
            for l in lines:
                cur_l=Polyline(l[0],l[1])
                cur_layer.AddGeometry(cur_l,dict(zip([attr[0] for attr in attr_info],l[3:])))
        elif layer_type=='POLYGON':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            polygons=self.cur.fetchall()
            for pg in polygons:
                cur_pg=Polygon(pg[0],pg[1])
                cur_layer.AddGeometry(cur_pg,dict(zip([attr[0] for attr in attr_info],pg[3:])))

        elif layer_type=='MULTIPOLYGON':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            mpolygons=self.cur.fetchall()
            for mpg in mpolygons:
                cur_mpg=MultiPolygon(mpg[0],mpg[1])
                cur_layer.AddGeometry(cur_mpg,dict(zip([attr[0] for attr in attr_info],mpg[3:])))
        elif layer_type=='MULTILINESTRING':
            self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
            mlines=self.cur.fetchall()
            for ml in mlines:
                cur_ml=MultiPolyline(ml[0],ml[1])
                cur_layer.AddGeometry(cur_ml,dict(zip([attr[0] for attr in attr_info],ml[3:])))
        else:
            pass
        return cur_layer

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
        layer_name='polygons'
        col_name='geom'
        self.cur.execute(f"select st_astext({col_name}),* from {layer_name};")
        attr_info=self.cur.fetchall()
        return attr_info


if __name__=="__main__":
    dbm=DBM()
    print(dbm.get_layers_list())
    a=dbm.load_layer('polygons')
    print(a)