# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HipdaspyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    author=scrapy.Field()
    postTime=scrapy.Field()
    link=scrapy.Field()
    tid=scrapy.Field()
    click=scrapy.Field()
    reply=scrapy.Field()
    spyTime=scrapy.Field();
    pass



class replyItem(scrapy.Item):
    author=scrapy.Field()
    postTime=scrapy.Field()
    content=scrapy.Field()
    tid=scrapy.Field()
    floor_number=scrapy.Field()
    pass


