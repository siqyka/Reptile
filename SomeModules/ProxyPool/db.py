# from getproxy import *
from config import *
import pymongo
import pymysql
# import redis

class SaveToDatabase():
    def __init__(self,type='mysql', host=DBMESSAGE['host'], port=DBMESSAGE['port'], username=DBMESSAGE['username'] ,\
                password=DBMESSAGE['password'],db=DBMESSAGE['db'],charset=DBMESSAGE['charset']):
        self.type=type
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.db=db
        self.charset=charset
        self.linkdb()


    def linkdb(self):
        if self.type=='mysql':
            self.connect = pymysql.Connect(host=self.host,port=self.port,
                user=self.username,passwd=self.password,
                db=self.db,charset=self.charset
                )
            self.cursor = self.connect.cursor()

    def set(self):
        pass

    def get(self):
        pass
    
    def delete(self):
        pass
    
    def all(self):
        pass

    def count(self):
        pass

    def random(self):
        pass



if __name__ == '__main__':
    SaveToDatabase()


