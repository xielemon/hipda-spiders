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
        'database': 'hipda2',
        'charset': 'utf8'
    }
    conn=0
    reply_list=[]


    def __init__(self):
        super(HipdaspyPipeline, self).__init__()
        self.logger=logging.getLogger(type(self).__name__)
        self.conn=mysql.connector.connect(**self.config)




    def process_item(self, item, spider):

        if isinstance(item,HipdaspyItem):
            try:
                cur=self.conn.cursor()
                sql="insert into post_list (title,author,postTime,link,tid) VALUES (%s,%s,%s,%s,%s)"
                map=(item['title'],item['author'],item['postTime'],item['link'],item['tid'])
                cur.execute(sql,map)
                #auto commit is off
                self.conn.commit()
            except mysql.connector.Error as e:
                print('insert datas error!{}'.format(e))

        elif isinstance(item,replyItem):
            self.reply_list.append((item['author'],item['postTime'],item['content'],item['tid'],item['floor_number']))
            if(len(self.reply_list)>1000):
                self.batch_insert_reply()
                self.reply_list=[]



    def close_spider(self,spider):
        self.batch_insert_reply()



    def batch_insert_reply(self):
        sql="insert into reply_list (author,postTime,content,tid,floor_number) VALUES  (%s,%s,%s,%s,%s)"
        cur=self.conn.cursor()
        cur.executemany(sql,self.reply_list)
        self.conn.commit()

