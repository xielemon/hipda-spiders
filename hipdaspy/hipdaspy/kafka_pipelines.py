# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from kafka import KafkaProducer

from items import *
from scrapy.utils.serialize import ScrapyJSONEncoder
import mysql.connector

class KafkaPipelines(object):

    cnt=0
    logger=0




    def __init__(self):
        super(KafkaPipelines, self).__init__()
        self.logger=logging.getLogger(type(self).__name__)
        self.producer=KafkaProducer(bootstrap_servers="115.159.124.104:9092")
        self.encoder=ScrapyJSONEncoder()




    def process_item(self, item, spider):

        if isinstance(item,HipdaspyItem):
            serilizedData=self.encoder.encode(item)
            print(serilizedData)
            self.producer.send("hipda",serilizedData);
            self.producer.flush()




    def close_spider(self,spider):
        self.batch_insert_reply()




