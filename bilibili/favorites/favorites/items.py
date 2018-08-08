# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FavoritesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    belong=scrapy.Field()
    name=scrapy.Field()
    date=scrapy.Field()
    furl=scrapy.Field()
    
    view=scrapy.Field()
    favorite=scrapy.Field()
    author=scrapy.Field()
    pubdate=scrapy.Field()
