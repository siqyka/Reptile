import requests
import json
from urllib.parse import urlencode
from multiprocessing import Pool,Lock,Manager
import functools


class weiboajax(object):
    def __init__(self,uid,page):
        self.baseurl='https://m.weibo.cn/api/container/getIndex?'
        self.uid=uid
        self.page=page
        self.headers={
            'Host':'m.weibo.cn',
            'Referer': 'https://m.weibo.cn/u/'+self.uid,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

    #爬取ajax数据
    def getpage(self):
        params={
                'type':'uid',
                'value':self.uid,
                'containerid':'107603'+self.uid,
                'page':str(self.page)
            }

        url=self.baseurl+urlencode(params)
        try:
            res=requests.get(url,headers=self.headers)
            if res.status_code==200:
                return res.json()
        except requests.ConnectionError as e:
            print('Error:',e.args)

    #解析json数据
    def parsepage(self,json):
        if json:
            items=json.get('data').get('cards')
            for i in items:
                try:
                    item=i.get('mblog')
                    weibo={}
                    weibo['id']=item.get('id')
                    weibo['content']=item.get('text')
                    weibo['reposts']=item.get('reposts_count')
                    weibo['comments']=item.get('comments_count')
                    weibo['attitudes']=item.get('attitudes_count')
                    try:
                        msgs=item.get('pics')
                        images=[]
                        for msg in msgs:
                            image=msg.get('url')
                            images.append(image)
                            weibo['pics']=images
                    except:
                        weibo['pics']='null'
                    yield weibo
                except:
                    pass

    #存储数据
    def savepage(self,msg,lock):
        with open("weibo.json","a",encoding="utf-8") as f:
            f.write(json.dumps(msg,indent=2,ensure_ascii=False))
        



def main(lock,page):
    a=weiboajax('',page) #输入uid
    b=a.getpage()
    c=a.parsepage(b)
    for i in c:
        lock.acquire()
        a.savepage(i,lock)
        lock.release()

if __name__ == '__main__':
    #给资源加锁
    manager=Manager()
    lock=manager.Lock()
    mains=functools.partial(main, lock)   #传入锁
    #进程池
    p=Pool(4)
    p.map(mains,range(1,20))#输入需要爬取的页数+1
    p.close()   
    p.join()   


