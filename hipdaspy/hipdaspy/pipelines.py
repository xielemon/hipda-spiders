# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from items import *
import mysql.connector

class HipdaspyPipeline(object):

    cnt=0
    logger=0

    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'hipda',
        'charset': 'utf8'
    }


    def __init__(self):
        super(HipdaspyPipeline, self).__init__()
        self.logger=logging.getLogger(type(self).__name__)
        mysql.connector.connect(**self.config)



    def process_item(self, item, spider):

        if isinstance(item,HipdaspyItem):
            print item['tid']+":"+item['title']
        elif isinstance(item,replyItem):
            print "reply:"+item['tid']

