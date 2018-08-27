from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import requests
import jobdb


class Lagou():
    def __init__(self,timeout):
        self.timeout=timeout
        self.joburls=[]
        self.headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_ga=GA1.2.1667356220.1534744913; user_trace_token=20180820140128-7a53df3d-a43e-11e8-aa7e-5254005c3644; LGUID=20180820140128-7a53e264-a43e-11e8-aa7e-5254005c3644; LG_LOGIN_USER_ID=d2566edc4444535f8275a2584ffedc82715e3336a9af7a63; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; index_location_city=%E6%9D%AD%E5%B7%9E; hasDeliver=176; _gid=GA1.2.899023627.1535330620; LGSID=20180827084312-2d35639a-a992-11e8-b24a-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; JSESSIONID=ABAAABAAAGGABCBA337480FF494CC18B24A2CD5F7ACA127; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535074094,1535160887,1535330620,1535331307; _putrc=BE3CE0C96DF640E3; login=true; unick=%E6%88%9A%E7%9B%88%E5%87%AF; gate_login_token=b5e331caa789b8ba98a82cfe665f46fe8f850df77c275f13; TG-TRACK-CODE=index_search; _gat=1; SEARCH_ID=2c0418d54e5f49b1965e818a8fe2a236; LGRID=20180827091147-2b6ba2ad-a996-11e8-b24a-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1535332335',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')#不加载图片
        self.browser=webdriver.Chrome(chrome_options=chrome_options)
        # self.browser=webdriver.Chrome()#可视浏览器
        self.browser.set_page_load_timeout(self.timeout)
        self.wait=WebDriverWait(self.browser,self.timeout)

    def get_first_page(self,url,page):
        try:
            self.browser.get(url)
            if page>1:
                submit=self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.pager_next')))
                for i in range(page-1):
                    submit.click()
                    time.sleep(0.5)
                self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.pager_is_current'),str(page)))
        except:
            print('erorr')

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pager_next')))

        res=pq(self.browser.page_source)
        items=res('.p_top .position_link').items()
        for item in items:
            url=item.attr('href')
            self.joburls.append(url)
            # print(url)
        
        return self.joburls
    
    def get_jobmsg(self,url):
        try:
            res=requests.get(url,headers=self.headers)
            re=pq(res.text)
            sadd=re('.work_addr').text().split(' ')[-2]
            position=re('.job-name .name').text()
            company=re('#job_company .fl').text().split(' ')[0]
            salary=re('.job_request span').text().split(' ')[0]
            claim=",".join(re('.job_request span').text().split(' ')[3::2])
            dic={
                'sadd':sadd,
                'position':position,
                'company':company,
                'salary':salary,
                'claim':claim,
                'joburl':url
            }
            yield dic
        except:
            print('msgerorr')


def main():
    url='https://www.lagou.com/jobs/list_python?px=default&city=%E6%9D%AD%E5%B7%9E#filterBox'
    lagou=Lagou(30)
    db=jobdb.SaveToDatabase(password='tarena')
    for i in range(1,2):
        lagou.get_first_page(url,i)

    for x in lagou.joburls:
        datas=lagou.get_jobmsg(x)
        for data in datas:
            db.set(data)

if __name__ == '__main__':
    main()