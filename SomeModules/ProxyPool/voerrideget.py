from pyquery import PyQuery as pq
import requests
from config import *
from getproxy import *

class XCGetProxy(GetProxy):
    def __init__(self):
        GetProxy.__init__(self)


    def getproxy(self,url):
        print(url)
        headers=HEADERS
        res=requests.get(url,headers=headers)
        html=pq(res.text)
        items=html('#ip_list tr').items()
        for  item in items:
            iproxy={
                "ip":item('td:nth-child(2)').text(),
                "port":item('td:nth-child(3)').text(),
            }
            # iproxy=[item('td:nth-child(2)').text()+":"+item('td:nth-child(3)').text()]
            self.arr.append(iproxy)