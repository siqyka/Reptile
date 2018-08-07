# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#抓取的信息有  项目所属页数、项目名称、项目链接、项目简介、项目的tag、项目的主语言、项目的stars数
class GayhubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ranking=scrapy.Field()
    name=scrapy.Field()
    link=scrapy.Field()
    synopsis=scrapy.Field()
    tags=scrapy.Field()
    language=scrapy.Field()
    stars=scrapy.Field()
