# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from urllib.parse import urlencode
from gayhub.items import GayhubItem
import re
import json

class Gayhubtop100Spider(Spider):
    name = 'gayhubtop100'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']


    def parse(self, response):
        itemss=response.css('.repo-list-item')
        for items in itemss:
            tags=[]
            item=GayhubItem()
            item['name']=items.css('h3 a::text').extract_first()
            item['link']='https://github.com/'+items.css('h3 a::attr(href)').extract_first()
            item['synopsis']=items.css('.col-12 .d-inline-block::text').extract_first().split()
            for i in items.css('.topic-tag::text').extract():
                i=i.strip()
                tags.append(i)
            item['tags']=tags
            try:
                item['language']=items.css('.flex-shrink-0 .text-gray::text').extract()[1].strip()
            except:
                item['language']='null'
            item['stars']=items.css('.flex-shrink-0 .pl-2 a::text').extract()[1].strip()
            # 通过特殊处理 页数加结果页面定位数的方式输出项目排名
            page=int(re.findall(r'Repositories&p=(.*)',response.url)[0])-1
            result_position=json.loads(items.css('h3 a::attr(data-hydro-click)').extract_first())['payload']['result_position']
            if result_position==10:
                item['ranking']=str(page+1)+'0'
            else:
                item['ranking']=str(page)+str(result_position)

            yield item
            
            

    def start_requests(self):
        data={
            'o':'desc',
            'q':self.settings.get('python'),
            's':'stars',
            'type':'Repositories'
        }
        pages=self.settings.get('MAX_ITEMS')//10+1   #计算抓取几页
        base_url='https://github.com/search?'
        for page in range(1,pages):
            data['p']=page
            params=urlencode(data)
            url=base_url+params
            yield Request(url,self.parse)
