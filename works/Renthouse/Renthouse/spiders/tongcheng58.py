# -*- coding: utf-8 -*-
import scrapy
import Renthouse.settings as settings
from Renthouse.items import RenthouseItem

class A58tongchengSpider(scrapy.Spider):
    name = 'tongcheng58'
    allowed_domains = ['www.58.com']
    start_urls = ['http://www.58.com/']

    def parse(self, response):
        print(response.url)
        items=response.css('.listUl li')
        data=RenthouseItem()
        for item in items:
            title=item.css('.des h2 a::text').extract_first()
            if title is not None:
                title = title.strip()
            else:
                title=item.css('.des h2 a::text').extract()
            data['tltie']=title

            try:
                radd=item.css('.des .add a::text').extract()[-1]
                if '...'in radd:
                    radd=radd[:-3]
                data['radd']=radd
            except:
                data['radd']=item.css('.des .add a::text').extract()

            geren1=item.css('.des .geren span::text').extract_first()
            geren2=item.css('.des .geren::text').extract()[-1].strip()
            data['geren']=geren1+geren2

            data['money']=item.css('.money b::text').extract_first()
            data['rurl']=item.css('.des h2 a::attr(href)').extract_first()
            yield data


    def start_requests(self):
        for page in range(1,settings.MAX_PAGE+1):
            url='http://hz.58.com/%schuzu/0/pn%s/?minprice=%s_%s'%(settings.AREA,page,settings.MIN_MONEY,settings.MAX_MONEY)
            yield scrapy.Request(url=url,callback=self.parse)