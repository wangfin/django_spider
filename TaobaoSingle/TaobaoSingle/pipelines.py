# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import os
from pybloom import BloomFilter
import hashlib
from TaobaoSingle.items import TaobaosingleItem
from .handledb import MysqldbHelper

mysql = MysqldbHelper()

class TaobaosinglePipeline(object):
    def __init__(self):

        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.brandName = 'mybloom'

    def open_spider(self, spider):
       pass

    def close_spider(self, spider):
        """
        called when spider is closed.
        do something after pipeline processing all items.
        example: close the database.
        """
        spider.logger.debug("close mysql")
        mysql.close()
        spider.logger.debug("close mysql")
        return

    def process_item(self, item, spider):
        if isinstance(item, TaobaosingleItem):
            #token = item['product_url'] + item['ActualPrice']
            #m = hashlib.md5()
            #m.update(token)
            #encodeStr = m.hexdigest()
            #flag = self.bf.add(encodeStr)
            # 当前item没有在bloomfilter中，便将其收集下来，视为增量
            #if flag == False:
            sql = "insert into tbproduct(itemid,url,names,price,actualprice,allcount,goodcount,aftercount,generalcount,poorcount,sellerlink,sellerNick,imgurl) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  "" % (item['product_id'], item['product_url'], item['product_name'].strip(), item['Price'],
                        item['ActualPrice'],
                        item['AllCount'], item['GoodCount'], item['AfterCount'], item['GeneralCount'],
                        item['PoorCount'],
                        item['sellerlink'], item['sellerNick'],item['img_url'])
            mysql.update(sql)
            return item



