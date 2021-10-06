import psycopg2
from Layer import *
from Geometry import *

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
        return self.layer_list

    def add_layer_from_memory(self,layer:Layer):
        if layer.name in self.get_layers_list():
            self.cur.execute(f"drop table {layer.name}")
        self.create_table(layer.name,layer.type,layer.srid,layer.attr_desp_dict)
        for geometry in layer.geometries:
            wkt=geometry.ToWKT()
            self.cur.execute(f"""insert into {layer.name}(geom,{','.join([k for k in layer.attr_desp_dict.keys()])}) 
            values({wkt},{geometry.other_attr})""")
            pass
        self.cur.commit()
        pass

    def add_layer_from_shp(self):
        pass

    def create_table(self,tablename,geom_type,srid,**kwargs):
        self.cur.execute(f"""
            create table {tablename}(
                sid serial primary key,
                geom Geometry({geom_type},{srid}),
                {''.join([f"{attr_name} {attr_type},\n" for attr_name,attr_type in kwargs])}
            )
        """)
    
    def insert_geometry(self,geomtry):
        pass
    
    # def execute(self,sql_str):
    #     self.cur.execute(sql_str)

    # def commit(self):
    #     self.cur.commit()

    def test(self):
        # self.cur.execute("""
        #     select * from spatial_ref_sys limit 10;
        # """)
        rows=self.cur.fetchall()
        return rows


if __name__=="__main__":
    dbm=DBM()
    dbm.get_layers_list()
    a=dbm.test()
    print(a)