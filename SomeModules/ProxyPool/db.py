# from getproxy import *
from config import *
import pymongo
import pymysql
import redis
import random

class SaveToDatabase():
    def __init__(self,type='mysql', host=DBMESSAGE['host'], port=DBMESSAGE['port'], username=DBMESSAGE['username'] ,
                password=DBMESSAGE['password'],db=DBMESSAGE['db'],table=DBMESSAGE['table'],
                charset=DBMESSAGE['charset']):
        self.type=type
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.db=db
        self.charset=charset
        self.table=table
        self.linkdb()


    def linkdb(self):
        if self.type=='mysql':
            sql="create table if not exists {0}(id int not null auto_increment primary key,{1} \
                varchar(40),{2} varchar(40)),{3} varchar(40)".format(self.table,TABLE[0],
                TABLE[1],TABLE[2]
                )
            try:
                self.connect = pymysql.Connect(host=self.host,port=self.port,
                    user=self.username,passwd=self.password,
                    db=self.db,charset=self.charset
                    )
                self.cursor = self.connect.cursor()
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                except:
                    self.connect.rollback()
            except:
                self.connect = pymysql.Connect(host=self.host,port=self.port,
                    user=self.username,passwd=self.password,
                    charset=self.charset
                    )
                self.cursor = self.connect.cursor()
                try:
                    self.cursor.execute('create database {0};'.format(self.db))
                    self.cursor.execute('use {0}'.format(self.db))
                    self.cursor.execute(sql)
                    self.connect.commit()
                except Exception as e:
                    self.connect.rollback()
                    print(e)                    

        elif self.type=='mango':
            client = pymongo.MongoClient(host=self.host, port=self.port)
            self.db = client[self.db]

        elif self.type=='redis':
            self.redis = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def set(self,data):
        if self.type=='mysql':
            keys=",".join(data.keys())
            values=",".join(["%"]*len(data))
            sql="inster into {table} ({keys}) values({values})".format(table=self.table,keys=keys,values=values)
            try:
                if self.cursor.execute(sql,tuple(data.values())):
                    print('inster success')
                    self.connect.commit()
            except:
                print("inster failed")
                self.connect.rollback()

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            pass

    def delete(self,ip):
        if self.type=='mysql':
            sql="delete from {0} where ip={1}".format(self.table,ip)
            try:
                self.cursor.execute(sql)
                return True
            except:
                return False

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            pass
    
    def all(self):
        if self.type=='mysql':
            sql="select * from {0}".format(self.table)
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                return result
            except:
                return "error"

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            pass

    def count(self):
        if self.type=='mysql':
            sql="select count(*) from {0}".format(self.table)
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                return result[0][0]
            except:
                return "error"

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            pass

    def random(self):
        if self.type=='mysql':
            sql1="select count(*) from {0}".format(self.table)
            try:
                self.cursor.execute(sql1)
                result = self.cursor.fetchall()[0][0]
                id=random.randint(1,result)
                sql2="select ip,port from {0} where id={1}".format(self.table,id)
                proxy=self.cursor.fetchone()
                return proxy
            except:
                return "error"

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            pass

    def batch(self, count, start, stop=0):
        if self.type=='mysql':
            proxyl=[]
            sql1="select ip,port from {0} limit{1},{2}".format(self.table,start,count)
            try:
                self.cursor.execute(sql1)
                proxys=self.cursor.fetchall()
                for item in proxys:
                    proxyl.append(item[0]+":"+item[1])
                return proxyl
            except:
                return proxyl

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            pass
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    SaveToDatabase()


