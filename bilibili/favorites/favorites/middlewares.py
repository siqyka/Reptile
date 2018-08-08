# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import getLogger
from scrapy.http import HtmlResponse
import time

import sys
sys.path.append(r'D:\GIT\Reptile\bilibili')#bilibili_Verification模块所在文件夹路径
import bilibili_Verification


class FavoritesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    def __init__(self,timeout=None,url=''):
        self.logger=getLogger(__name__)
        self.timeout=timeout
        self.url=url
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')#不加载图片
        self.browser=webdriver.Chrome(chrome_options=chrome_options)
        # self.browser=webdriver.Chrome()#可视浏览器
        self.browser.set_page_load_timeout(self.timeout)
        self.wait=WebDriverWait(self.browser,self.timeout)

    def __del__(self):
        self.browser.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(timeout=crawler.settings.get('SELRNIUM_TIMEOUT'),
                url=crawler.settings.get('URL')
                # service_args=crawler.settings.get('')
                )
        return s


    def process_request(self, request, spider):
        item = request.meta.get('item')

        try:
            self.browser.get(request.url)

            # bili=bilibili_Verification.bilibili(bro=self.browser,
            #                                     timeout=self.timeout,url=request.url)
            # bili.webbro()
            # bili.input_msg('123','456')
            # bili.get_jyimage()
            # bili.get_q_jyimage()
            # bili.move()
            # self.wait.until(EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, '.nav-con .fr .nav-item .t')))
            # btn=self.browser.find_elements_by_css_selector('.nav-con .fr .nav-item .t')[5]
            # btn.click()
            # print(self.browser.page_source)

            self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.be-scrollbar .fav-list')))
            time.sleep(2)
            lis=self.browser.find_elements_by_css_selector('.be-scrollbar .fav-list .fav-item a')
            lis[item].click()
            self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.fav-content')))
            time.sleep(3)
            return HtmlResponse(url=request.url, body=self.browser.page_source, 
                                    request=request, encoding='utf-8', status=200)
        except:
            return HtmlResponse(url=request.url, request=request, status=500)
