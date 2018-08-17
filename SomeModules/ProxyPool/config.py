HEADERS={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }


WEBSITE=[]
for offset in range(1,3):
        url='http://www.xicidaili.com/nn/'+str(offset)
        WEBSITE.append(url)

DBMESSAGE={
        'host':'localhost',
        'port':'3306',
        'username':'',
        'password':'',
        'db':'test',
        'charset':'utf8'
}