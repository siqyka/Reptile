# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection=table='comment'
    storename = scrapy.Field()
    reviewnum = scrapy.Field()
    percapita = scrapy.Field()
    storetype = scrapy.Field()
    addr = scrapy.Field()
    recommend = scrapy.Field()
    evaluate = scrapy.Field()
    storeurl = scrapy.Field()
