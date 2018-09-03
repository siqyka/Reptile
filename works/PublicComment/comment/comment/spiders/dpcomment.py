# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy
import comment.settings as settings
from comment.items import CommentItem


class DpcommentSpider(scrapy.Spider):
    name = 'dpcomment'
    allowed_domains = ['http://www.dianping.com/hangzhou/ch10/o3']
    start_urls = ['http://http://www.dianping.com/hangzhou/ch10/o3/']

    def parse(self, response):
        if response.status == 200:
            data = CommentItem()
            items = response.css('#shop-all-list li')
            for item in items:
                data['storename'] = item.css('.tit h4::text').extract_first()
                data['reviewnum'] = item.css('.review-num b::text').extract_first()
                data['percapita'] = item.css('.mean-price b::text').extract_first()[1::]
                data['storetype'] = item.css('.tag-addr .tag::text').extract_first()
                data['addr'] = item.css('.tag-addr .addr::text').extract_first()
                data['recommend'] = ','.join(item.css('.recommend a::text').extract())
                
                #评分分开
                # evaluate1 = item.css('.comment-list span::text').extract()
                # evaluate2 = item.css('.comment-list span b::text').extract()
                # evaluate=[]
                # for i in range(len(evaluate1)):
                #     evaluate.append('%s:%s'%(evaluate1[i],evaluate2[i]))
                # data['evaluate']=','.join(evaluate)

                #综合评分
                evaluate2 = item.css('.comment-list span b::text').extract()
                evaluate=0
                for i in evaluate2:
                    i=float(i)
                    evaluate+=i
                data['evaluate']=str(round(evaluate/3,2))
                data['storeurl'] = item.css('.txt .tit a::attr(href)').extract_first()
                yield data

    def start_requests(self):
        for page in range(1, settings.MAX_PAGE + 1):
            url = 'http://www.dianping.com/%s/ch10/o3p%s' % (settings.CITY,str(page))
            yield scrapy.Request(url=url, callback=self.parse)
