# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class CommentPipeline(object):
    def __init__(self,host,database,user,password,port):
        self.host=host
        self.database=database
        self.user=user
        self.password=password
        self.port=port

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWOED'),
            port=crawler.settings.get('MYSQL_PROT')
        )
        return s

    def process_item(self, item, spider):
        data=dict(item)
        keys=','.join(data.keys())
        values=','.join(['%s']*len(data))
        sql='insert into %s (%s,%s) values (%s,%s)'%(item.table,keys,'id',values,'null')
        # sql='insert into %s values (%s)'%(item.table,values)
        # print(sql)
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item

    def open_spider(self,spider):
        self.db=pymysql.connect(self.host,self.user,self.password,self.database,charset='utf8',port=self.port)
        self.cursor=self.db.cursor()

    def close_spider(self,spider):
        self.db.close()