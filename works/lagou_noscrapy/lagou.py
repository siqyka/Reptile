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
            'Cookie': '',
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
                ypage=self.browser.find_element_by_class_name("pager_is_current").text

                submit=self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.next_disabled')))
                for i in range(page-int(ypage)):
                    submit.click()
                    time.sleep(0.5)
                self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'.pager_is_current'),str(page)))
        except Exception as e:
            print('erorr',e)

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.s_position_list ')))

        res=pq(self.browser.page_source)
        items=res('.p_top .position_link').items()
        for item in items:
            url=item.attr('href')
            self.joburls.append(url)
        
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
    db=jobdb.SaveToDatabase()
    for i in range(1,2):
        lagou.get_first_page(url,i)

    for x in lagou.joburls:
        datas=lagou.get_jobmsg(x)
        for data in datas:
            db.set(data)

if __name__ == '__main__':
    main()