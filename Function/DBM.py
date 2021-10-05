import psycopg2

class DBM:
    def __init__(self) -> None:
        self._connect()
        pass

    def _connect(self):
        self.conn=psycopg2.connect(database="minigis",user="minigiser",password="minigis",host="47.104.149.94",port="5432")
        self.cur=self.conn.cursor()

    def test(self):
        self.cur.execute("""
            select * from spatial_ref_sys limit 10;
        """)
        rows=self.cur.fetchall()
        return rows

if __name__=="__main__":
    dbm=DBM()
    a=dbm.test()
    print(1)