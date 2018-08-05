import requests
from pyquery import PyQuery as pq
from lxml import etree
import json


'''
登录git并搜索python后爬取Star最多的100个项目
吐槽：兔国上gayhub还是慢，爬取也慢，能用代理就代理把
'''

class Login():
    def __init__(self,items=10,flag='python'):
        self.headers={
                'Host': 'github.com',
                'Referer': 'https://github.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        self.login_url='https://github.com/login'   #登陆页
        self.post_url='https://github.com/session'  #登录数据发送地址
        self.uname=''     #账号
        self.upwd=''       #密码
        self.session=requests.Session()
        self.page=items//10+1   #爬取的页数
        self.flag=flag     #爬取输入的关键字

    #获取登录需要的authenticity_token
    def login_msg(self):
        res=self.session.get(self.login_url)
        sel=etree.HTML(res.text)
        token=sel.xpath('//div//input/@value')[1]
        # print(token)
        return token

    #登录操作
    def login(self):
        #post上传的数据
        post_data={
            'commit':'Sign in',
            'utf8':'✓',
            'authenticity_token':self.login_msg(),
            'login':self.uname,
            'password':self.upwd
        }

        res=self.session.post(self.post_url, data=post_data, headers=self.headers)
        print(res.status_code)
        if res.status_code==200:
            self.first_hundred()

    #爬取关键词的前n项
    def first_hundred(self):
        # print('123')
        for i in range(1,self.page+1):
            url='https://github.com/search?o=desc&p=%s&q=%s&s=stars&type=Repositories'%(i,self.flag)
            # print(url)
            res=self.session.get(url)
            if res.status_code==200:
                re=pq(res.text)
                lis=re(".repo-list-item").items()
                for i in lis:
                    item={
                    #项目名称
                    "name":i.find("h3 a").text(),
                    #项目链接
                    "link":i.find("h3 a").attr.href,
                    #项目简介
                    "synopsis":i.find(".col-12 .d-inline-block").text(),
                    #项目使用语言
                    "language":i.find(".repo-language-color").parent().text(),
                    #项目星数
                    "Stars":i.find(".flex-shrink-0 .pl-2").text()
                    }
                    self.save_msg(item)
            else:
                print("第"+i+"页爬取不成功")

    #存储数据
    def save_msg(self,item):
        with open('git_first_hundred1.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(item,indent=2,ensure_ascii=False))
            f.write('\n')

def main():
    git=Login(10,'python')
    git.login()

if __name__ == '__main__':
    main()