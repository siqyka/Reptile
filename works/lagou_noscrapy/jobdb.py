import pymysql

class SaveToDatabase():
    def __init__(self, host='localhost', port=3306, username='root' ,
                password='123456',db='work',table='works_jobs',):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.db=db
        self.table=table
        self.linkdb()

    def linkdb(self):
        self.connect = pymysql.Connect(host=self.host,port=self.port,
                    user=self.username,passwd=self.password,db=self.db)
        self.cursor = self.connect.cursor()               

    #插入数据
    def set(self,data):
        keys=",".join(data.keys())
        values=",".join(['%s']*len(data))
        sql="insert into {table} ({keys},{id}) values({values},{vid})".format(table=self.table,keys=keys,values=values,id='id',vid='null')    
        try:
            if self.cursor.execute(sql,tuple(data.values())):
                print('insert success')
                self.connect.commit()
        except:
            print("insert failed")
            self.connect.rollback()