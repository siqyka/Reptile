# -*- coding: utf-8 -*-
import scrapy
from LaGou.items import LagouItem
import LaGou.settings as settings


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com']
    start_urls = ['http://https://www.lagou.com/']

    def parse(self, response):
        if response.status==200:
            items=response.css('ul .con_list_item')
            data=LagouItem()
            for item in items:
                data['position']=item.css('.p_top .position_link h3::text').extract_first()
                data['company']=item.css('.company_name a::text').extract_first()
                data['sadd']=item.css('.p_top .add em::text').extract_first()
                data['salary']=item.css('.li_b_l .money::text').extract_first()
                data['claim']=item.css('.p_bot .li_b_l::text').extract()[-1].strip()
                # data['tags']=item.css('.list_item_bot .li_b_l span::text').extract()
                data['joburl']=item.css('.p_top .position_link::attr(href)').extract_first()
                yield data



    def start_requests(self):
        for page in range(3,settings.MAX_PAGE+1):
            url='https://www.lagou.com/jobs/list_%s?city=%s&cl=false&fromSearch=true'%(settings.KEY,settings.CITY)   #输入uid
            yield scrapy.Request(url=url,callback=self.parse,meta={'page':page},dont_filter=True)