# -*- coding: utf-8 -*-
import scrapy
from favorites.items import FavoritesItem


class MyfavoritesSpider(scrapy.Spider):
    name = 'MyFavorites'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']

    def parse(self, response):
        if response.status==200:
            items=response.css(".fav-video-list li")
            belong=response.css('.breadcrumb .cur::text').extract_first()
            data=FavoritesItem()
            for i in items:
                data['belong']=belong
                data['name']=i.css('.title::attr(title)').extract_first()
                if not data['name']:
                    continue
                data['date']=i.css('.meta::text').extract_first().split()
                data['furl']=i.css('.title::attr(href)').extract_first()
                data['author']=i.css('.meta-mask .meta-info .author::text').extract_first()
                data['pubdate']=i.css('.meta-mask .meta-info .pubdate::text').extract_first()
                data['view']=i.css('.meta-mask .meta-info .view::text').extract_first()
                data['favorite']=i.css('.meta-mask .meta-info .favorite::text').extract_first()
                yield data


    def start_requests(self):
        for item in range(20):
            url='https://space.bilibili.com/4912884/#/favlist'
            yield scrapy.Request(url=url,callback=self.parse,meta={'item':item},dont_filter=True)