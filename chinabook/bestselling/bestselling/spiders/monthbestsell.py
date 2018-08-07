# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from bestselling.items import BestsellingItem

class MonthbestsellSpider(Spider):
    name = 'monthbestsell'
    allowed_domains = ['http://www.bookschina.com/24hour/30_0_1']
    start_urls = ['http://http://www.bookschina.com/24hour/30_0_1/']

    def parse(self, response):
        items=response.css('.bookList li')
        for item in items:
            data=BestsellingItem()
            data=item.css('')


    def start_requests(self):
        pages=self.settings.get('MAX_ITEM')//30+1
        choice=self.settings.get('CHOICE')
        for page in range(1,pages):
            url='http://http://www.bookschina.com/24hour/%s_0_'%choice+str(page)
            yield Request(url=url,callback=self.parse)