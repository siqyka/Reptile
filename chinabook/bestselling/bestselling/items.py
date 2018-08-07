# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestsellingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookname=scrapy.Field()
    bookurl=scrapy.Field()
    author=scrapy.Field()
    publisher=scrapy.Field()
    sellprice=scrapy.Field()
    price=scrapy.Field()
    discount=scrapy.Field()
    comment=scrapy.Field()
    ranking=scrapy.Field()
