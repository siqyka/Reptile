# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from bestselling.items import BestsellingItem

class MonthbestsellSpider(Spider):
    name = 'monthbestsell'
    allowed_domains = ['http://www.bookschina.com/24hour/30_0_1']
    start_urls = ['http://http://www.bookschina.com/24hour/30_0_1/']

    def parse(self, response):
        if response.status==200:
            items=response.css('.bookList li')
            for item in items:
                data=BestsellingItem()
                data['bookname']=item.css('.name a::text').extract_first()
                data['bookurl']='http://www.bookschina.com/'+item.css('.name a::attr(href)').extract_first()
                data['author']=item.css('.author a::text').extract_first()
                data['publisher']=item.css('.publisher a::text').extract_first()
                data['sellprice']=item.css('.sellPrice::text').extract_first()
                data['price']=item.css('.priceWrap del::text').extract_first()
                data['discount']=item.css('.discount::text').extract_first()
                data['comment']=item.css('.startWrap a::text').extract_first()
                data['ranking']=item.css('.num span::text').extract_first()
                yield data


    def start_requests(self):
        pages=self.settings.get('MAX_ITEM')%30
        if pages==0:
            pages=self.settings.get('MAX_ITEM')//30+1
        else:
            pages=self.settings.get('MAX_ITEM')//30+2

        choice=self.settings.get('CHOICE')
        for page in range(1,pages):
            url='http://www.bookschina.com/24hour/%s_0_'%choice+str(page)
            # url='http://www.bookschina.com/24hour/30_0_1'
            yield Request(url=url,callback=self.parse,meta={'page':page})