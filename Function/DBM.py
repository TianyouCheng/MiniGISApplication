import psycopg2
from .Layer import *
from .Geometry import *

"""
矢量数据的属性字段，支持varchar，
"""

class DBM:
    def __init__(self) -> None:
        self._connect()
        pass

    def _connect(self):
        self.conn=psycopg2.connect(database="minigis",user="minigiser",password="minigis",host="47.104.149.94",port="5432")
        self.cur=self.conn.cursor()

    def get_layers_list(self):
        sql=f"""
            select tablename from pg_tables
            where tablename not like 'pg_%'
            and tablename not like 'sql_%'
            and tablename not like 'spatial_ref_sys';
        """
        self.cur.execute(sql)
        # self.layer_list= self.cur.fetchall()
        return self.cur.fetchall()

    def add_layer_from_memory(self,layer:Layer):
        if layer.name in self.get_layers_list():
            self.cur.execute(f"drop table {layer.name}")
        self.create_table(layer.name,layer.type,layer.srid,layer.attr_desp_dict)
        for geometry in layer.geometries:
            self.insert_geometry(layer,geometry)
        self.conn.commit()

    def add_layer_from_shp(self):
        pass

    def create_table(self,tablename,geom_type,srid,**kwargs):
        sql=f"""
            create table {tablename}(
                gid int primary key,
                geom Geometry({geom_type},{srid})
                {''.join([f',{attr_name} {attr_type}' for attr_name,attr_type in kwargs])}
            );
        """
        self.cur.execute(sql)
    
    def insert_geometry(self,layer:Layer,geomtry:Geometry):
        wkt=geomtry.ToWkt()
        sql=f"""
            insert into {layer.name}(id,geom,{','.join([k for k in layer.attr_desp_dict.keys()])})
            values({geomtry.ID},st_geometryfromtext(\'{wkt}\',{layer.srid}),{','.join(layer.get_attr(geomtry.ID))});
        """
        self.cur.execute(sql)
    
    def load_layer(self,layer_name):
        self.cur.execute(f"select f_geometry_column,srid,type from geometry_columns where f_table_name='{layer_name}'; ")
        col_name,layer_srid,layer_type=self.cur.fetchall()[0]
        cur_layer=Layer(layer_type,layer_name,layer_srid)
        #获取属性字段元数据
        # self.cur.execute(f"select * from {layer_name};")#geometry转为其他类型
        # geoms=self.cur.fetchall()
        #根据不同数据类型读取几何信息，addgeomtry
        if layer_type=='POINT':
            self.cur.execute(f"select st_x(geom),st_y(geom),* from {layer_name};")
            points =self.cur.fetchall()
            for p in points:
                cur_p=PointD(p[0],p[1],p[2])
                cur_layer.AddGeometry(cur_p,p[3:])
        elif layer_type=='LINESTRING':
            self.cur.execute(f"select st_astext(geom),* from {layer_name};")
            
            pass
        elif layer_type=='POLYGON':
            pass
        elif layer_type=='MULTIPOLYGON':
            pass
        elif layer_type=='MULTILINESTRING':
            pass
        else:
            pass
        # for geom in geoms:
        #     cur_geom=None
            
        #     cur_layer.AddGeometry()
        pass
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
        self.cur.execute(f"select st_x(geom),st_y(geom),* from test;")
        rows=self.cur.fetchall()
        return rows


if __name__=="__main__":
    dbm=DBM()
    print(dbm.get_layers_list())
    a=dbm.test()
    print(a[0])