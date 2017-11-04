# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from scrapy.exceptions import DropItem
import MySQLdb

# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)

class JdcommentsPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "jingdongcat":
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
            cur = conn.cursor(MySQLdb.cursors.DictCursor)

            name = item['name']
            url = item['url']
            _id = item['_id']
            sql = "insert into Jdmenu (names,url,_id) values ('%s','%s','%s')" % (name, url, _id)
            cur.execute(sql)
            conn.commit()

            return item
        # else:
        #     raise DropItem("Missing price in %s" % item)
            cur.close()
            conn.close()
        elif spider.name == "jingdongproducts":
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            print u'进入产品入库'

            taskid = r.get('jd_taskid')
            name = item['product_name'].strip() 
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
            try:
                sql = "insert into jdproducts (taskid,names,url,_id,reallyPrice,originalPrice,favourableDesc1,AllCount,GoodCount,AfterCount,GeneralCount,PoorCount) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    taskid,name, url, _id, reallyPrice, originalPrice, favourableDesc1, AllCount, GoodCount, AfterCount,
                GeneralCount, PoorCount)
                print sql
                cur.execute(sql)
                conn.commit()
                print u'插入数据库成功'
                return item
            except Exception as e:
                print('error:', e)
                conn.rollback()
            finally:
                cur.close()
                conn.close()
        elif spider.name == 'CSDNBlogCrawlSpider':
            f = open('info.txt', 'a')
            f.writelines('name:' + item['blog_name'] + '\n')
            f.writelines('url:' + item['blog_url'] + '\n')


