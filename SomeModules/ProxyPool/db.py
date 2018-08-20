from config import *
import pymongo
import pymysql
import redis
import random

class SaveToDatabase():
    def __init__(self,type=DBMESSAGE['dbtype'], host=DBMESSAGE['host'], port=DBMESSAGE['port'], username=DBMESSAGE['username'] ,
                password=DBMESSAGE['password'],db=DBMESSAGE['db'],table=DBMESSAGE['table'],
                charset=DBMESSAGE['charset']):
        self.type=type
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.db=db
        if type=='redis':
            self.db=REDIS_DB
        self.charset=charset
        self.table=table
        self.linkdb()

    #连接数据库
    def linkdb(self):
        if self.type=='mysql':
            sql="create table if not exists {0}(id int not null auto_increment primary key,{1} varchar(40),{2} varchar(40),unique ({3}))".format(self.table,TABLE[0],TABLE[1],TABLE[0])
            try:
                self.connect = pymysql.Connect(host=self.host,port=self.port,
                    user=self.username,passwd=self.password,
                    db=self.db,charset=self.charset
                    )
                self.cursor = self.connect.cursor()
                try:
                    self.cursor.execute(sql)
                    self.connect.commit()
                except :
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
            self.redis = redis.StrictRedis()

    #插入数据
    def set(self,data):
        if self.type=='mysql':
            keys=",".join(data.keys())
            values=",".join(['%s']*len(data))
            sql="insert into {table} ({keys}) values({values})".format(table=self.table,keys=keys,values=values)    
            try:
                if self.cursor.execute(sql,tuple(data.values())):
                    print('insert success')
                    self.connect.commit()
            except:
                print("insert failed")
                self.connect.rollback()

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            proxy=data['ip']+':'+data['port']
            self.redis.zadd(REDIS_KEY, 100, proxy)
            print("insert success")

    #删除数据
    def delete(self,ip):
        if self.type=='mysql':
            ips=ip.split(":")
            sql="delete from {0} where ip='{1}'".format(self.table,ips[0])
            print(sql)
            try:
                self.cursor.execute(sql)
                self.connect.commit()
                print('ok')
                return True
            except:
                self.connect.rollback()
                return False

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            self.redis.zrem(REDIS_KEY, ip)
            print('ok')
    
    #获得所用数据
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
            return self.redis.zrange(REDIS_KEY,0,-1)

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
            return self.redis.zcard(REDIS_KEY)

    #随机返回一个代理
    def random(self):
        if self.type=='mysql':
            sql1="select count(*) from {0}".format(self.table)
            try:
                self.cursor.execute(sql1)
                result = self.cursor.fetchall()[0][0]
                id=random.randint(1,result)
                sql2="select ip,port from {0}".format(self.table)
                self.cursor.execute(sql2)
                proxy=self.cursor.fetchall()
                rproxy=proxy[id][0]+":"+proxy[id][1]
                return rproxy
            except:
                return "error"

        elif self.type=='mango':
            pass

        elif self.type=='redis':
            result=self.redis.zrange(REDIS_KEY,0,-1)
            return random.choice(result)

    #批量返回代理
    def batch(self, count, start, stop=0):
        if self.type=='mysql':
            proxyl=[]
            sql1="select ip,port from {0} limit {1},{2}".format(self.table,start,count)
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
            return self.redis.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    SaveToDatabase()


