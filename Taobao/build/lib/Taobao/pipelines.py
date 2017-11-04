# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import string

import MySQLdb
import redis
from Taobao.handledb import MysqldbHelper
from Taobao.items import TaobaoProductItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from Taobao.items import DetailCategoryItem
from Taobao.items import TmallProductItem
# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)
class TaobaoPipeline(object):
    
    
    def open_spider(self, spider):
        """
        called when spider is opened.
        do something before pipeline is processing items.
        example: do settings or create connection to the database.
        """
        try:
            spider.logger.debug("trying to connect mysql")
            self.mysqlHelper = MysqldbHelper()
        except MySQLdb.DatabaseError:
            spider.logger.error("can not connect mysql")
            raise MySQLdb.DatabaseError
        return

    def close_spider(self, spider):
        """
        called when spider is closed.
        do something after pipeline processing all items.
        example: close the database.
        """
        spider.logger.debug("close mysql")
        self.mysqlHelper.close()
        return
    

    def process_item(self, item, spider):
        if isinstance(item, TaobaoProductItem):
            #print u'店铺的名字是',item['sellerNick']

            names = string.strip(item['product_name'])
            taskid = r.get("tb_taskid")

            sql = "insert into taobaoproduct(taskid,itemid,url,names,price,actualprice,allcount,goodcount,aftercount,generalcount,poorcount,sellerlink,sellerNick) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  ""%(taskid,item['product_id'],item['product_url'],names,item['Price'],item['ActualPrice'],
                      item['AllCount'],item['GoodCount'],item['AfterCount'],item['GeneralCount'],item['PoorCount'],
                      item['sellerlink'],item['sellerNick'])
            self.mysqlHelper.update(sql)
            return item

        if isinstance(item, TmallProductItem):
            #names = string.strip(item['product_name'])

            sql = "insert into tmallproduct(itemid,url,names,price,actualprice,allcount,goodcount,aftercount,generalcount,poorcount,sellerlink,sellerNick) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  "" % (
                  item['product_name'], item['product_url'], item['product_id'], item['defaultPrice'], item['num'],
                  item['Price'], item['seller_link'], item['CommentCount'], item['sellerName'])
            self.mysqlHelper.update(sql)

            return item
