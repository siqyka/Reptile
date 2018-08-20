from pyquery import PyQuery as pq
import requests
from config import *

#爬取代理程序，需重写getproxy方法
class GetProxy():
    def __init__(self):
        self.arr=[]

    def getproxy(self,url):
        raise NotImplementedError

    def run(self):
        for url in WEBSITE:
            self.getproxy(url)
        return self.arr

    

# class XCGetProxy(GetProxy):
#     def __init__(self):
#         GetProxy.__init__(self)


#     def getproxy(self,url):
#         print(url)
#         headers=HEADERS
#         res=requests.get(url,headers=headers)
#         html=pq(res.text)
#         items=html('#ip_list tr').items()
#         for  item in items:
#             iproxy={
#                 "ip":item('td:nth-child(2)').text(),
#                 "port":item('td:nth-child(3)').text(),
#             }
#             # iproxy=[item('td:nth-child(2)').text()+":"+item('td:nth-child(3)').text()]
#             self.arr.append(iproxy)
        

    

# if __name__ == '__main__':
#     b=XCGetProxy().run()
#     print(len(b))
    # for i in b:
    #     print(i)