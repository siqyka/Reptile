# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenthouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection=table='houses'
    title=scrapy.Field()
    rurl=scrapy.Field()
    radd=scrapy.Field()
    geren=scrapy.Field()
    money=scrapy.Field()
