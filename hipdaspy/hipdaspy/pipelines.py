# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from items import *

class HipdaspyPipeline(object):

    cnt=0
    logger=0


    def __init__(self):
        super(HipdaspyPipeline, self).__init__()
        self.logger=logging.getLogger(type(self).__name__)

    def process_item(self, item, spider):

        if isinstance(item,HipdaspyItem):
            print item['tid']+":"+item['title']
        elif isinstance(item,replyItem):
            print "reply:"+item['tid']

