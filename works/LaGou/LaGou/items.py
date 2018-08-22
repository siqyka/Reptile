# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection=table='jobs'
    position=scrapy.Field()
    company=scrapy.Field()
    sadd=scrapy.Field()
    salary=scrapy.Field()
    claim=scrapy.Field()
    # tags=scrapy.Field()
    joburl=scrapy.Field()
    


