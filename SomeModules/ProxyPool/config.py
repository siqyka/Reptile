#geetproxy.py

#请求头
HEADERS={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

#需要爬取代理的网页
WEBSITE=[]
for offset in range(1,3):
        url='http://www.xicidaili.com/nn/'+str(offset)
        WEBSITE.append(url)


#db.py

#数据库的信息
DBMESSAGE={
        'host':'localhost',
        'port':3306,
        'username':'',
        'password':'',
        'db':'db',
        'table':'test',
        'charset':'utf8'
}

#创建表所需的字段(需和代理爬取字段相同)
TABLE=['ip','porxy','type']


#detect.py

#代理测试连接
TEST_URL='https://www.baidu.com'

#请求正确的状态码
VALID_STATUS_CODES=[200,302]

#每次异步测试请求的个数
BATCH_TEST_SIZE=10


#run.py

#重写getproxy方法的文件名和类名
OVERRIDE_MODULE={
        'MODULENAME':'test',
        'CLASSNAME':'XCGetProxy'
}


