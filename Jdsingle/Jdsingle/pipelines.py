# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import os
from pybloom import BloomFilter
import hashlib
import pytz
from datetime import datetime

class JdsinglePipeline(object):
    def __init__(self):

        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.brandName = 'mybloom'

    def open_spider(self, spider):
        pass


    def process_item(self, item, spider):

        if spider.name == "jingdongcat":

            name = item['name']
            url = item['url']
            _id = item['_id']
            sql = "insert into Jdmenu (names,url,_id) values ('%s','%s','%s')" % (name, url, _id)
            self.cur.execute(sql)
            self.conn.commit()

            # return item
        # else:
        #     raise DropItem("Missing price in %s" % item)
        #     cur.close()
        #     conn.close()
        elif spider.name == "JdSingleSpider":

            # print u'进入产品入库'

            name = item['product_name']
            url = item['product_url']
            _id = item['product_id']
            reallyPrice = item['reallyPrice']
            originalPrice = item['originalPrice']
            favourableDesc1 = item['favourableDesc1']
            AllCount = item['AllCount']
            GoodCount = item['GoodCount']
            AfterCount = item['AfterCount']
            GeneralCount = item['GeneralCount']
            PoorCount = item['PoorCount']
            imgurl = item['image_url']
            tz = pytz.timezone('Asia/Shanghai')
            now = datetime.now(tz)
            now_time = now.strftime("%Y/%m/%d %H:%M:%S")
            try:
                # print u'插入数据库成功'

                #token = url + reallyPrice
                #m = hashlib.md5()
                #m.update(token)
                #encodeStr = m.hexdigest()
                #flag = self.bf.add(encodeStr)
                # 当前item没有在bloomfilter中，便将其收集下来，视为增量
                #if flag == False:
                sql = "insert into jdproduct (names,url,_id,reallyPrice,originalPrice,favourableDesc1,AllCount,GoodCount,AfterCount,GeneralCount,PoorCount,imgurl,time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (name, url, _id, reallyPrice, originalPrice, favourableDesc1, AllCount, GoodCount, AfterCount,GeneralCount, PoorCount,imgurl,now_time)
                    # print sql
                self.cur.execute(sql)
                self.conn.commit()
                    # print '插入文件'
                    # f = open('info.txt', 'a')
                    # f.writelines('name:' + url + '\n')
                    # f.writelines('url:' + reallyPrice + '\n')
                return item

            except Exception as e:
                print('error:', e)
                self.conn.rollback()
            # finally:
            #     cur.close()
            #     conn.close()
        elif spider.name == 'CSDNBlogCrawlSpider':
            f = open('info.txt', 'a')
            f.writelines('name:' + item['blog_name'] + '\n')
            f.writelines('url:' + item['blog_url'] + '\n')

    def close_spider(self, spider):
        """
        called when spider is closed.
        do something after pipeline processing all items.
        example: close the database.
        """
        spider.logger.debug("close mysql")
        self.cur.close()
        self.conn.close()
        #self.bf.tofile(open('mybloom' + '.blm', 'wb'))
        return

