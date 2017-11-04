# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

from handledb import MysqldbHelper
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.exceptions import DropItem
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

# 该类是为了获取爬取深度的页数
# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)

class News2MySQLPipeline(object):
    """
    save news item to mysql pipeline.
    """
    mysql_table = 'news'

    def __init__(self, ip, port, mysql_user, mysql_password, mysql_database):
        """
        set database information.
        """
        self.mysql_ip = ip
        self.mysql_port = int(port)
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

    def process_item(self, item, spider):
        """
        process each items from the spider.
        example: check if item is ok or raise DropItem exception.
        example: do some process before writing into database.
        example: check if item is exist and drop.
        """
        spider.logger.debug("parsing item before write mysql")
        if item["url"] is None:
            raise DropItem("invalid items url: %s" % str(item["url"]))

        taskid = r.get('wy_taskid')
        id = item['id']
        url = item["url"][0].strip().encode('UTF-8')

        try:
            source = item["source"][0].strip().encode('UTF-8')
        except:
            source = ""
        try:
            title = item["title"][0].strip().encode('utf-8')
        except:
            title = ""
        try:
            editor = item["editor"][0].strip().encode('UTF-8')
        except:
            editor = ""
        try:
            time_string = item["time"][0].strip().split()
            datetime = time_string[0] + ' ' + time_string[1]
            time = datetime.encode('utf-8')
        except:
            time = ""

        time_string = item["time"][0].strip().split()
        datetime = time_string[0] + ' ' + time_string[1]

        try:
            content = ""
            for para in item["content"]:
                content += para.strip().replace('\n', '').replace('\t', '')
            content = content.encode('UTF-8')


        except:
            content = ""



        text = content #codecs.open('../test/doc/02.txt', 'r', 'utf-8').read()
        tr4w = TextRank4Keyword()

        tr4w.analyze(text=text, lower=True, window=2) # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

        keywords = ""
        phrases = ""
        summary = ""
        #print('关键词：')
        for item in tr4w.get_keywords(10, word_min_len=1):
            keywords = keywords + item.word + "," #print(item.word, item.weight)

        #print()
        #print('关键短语：')
        for phrase in tr4w.get_keyphrases(keywords_num=10, min_occur_num=2):
            phrases = phrases + phrase + ","#print(phrase)

        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source='all_filters')

        #print()
        #print('摘要：')
        for item in tr4s.get_key_sentences(num=3):
            summary = summary + item.sentence + ","#print(item.index, item.weight, item.sentence)

        cursor = self.db.cursor()
        spider.logger.debug("trying to write mysql")
        sql = "INSERT INTO %s (TASKID,ID,URL, SOURCE, TITLE, EDITOR,\
            TIME, CONTENT,KEYWORDS,PHRASES,SUMMARY) \
            VALUES ('%s','%s','%s', '%s', '%s', '%s', '%s' ,'%s','%s','%s','%s')" % \
            (self.mysql_table, taskid,id, url, source, title, editor, time, content,keywords,phrases,summary)
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            spider.logger.error("failed to write mysql")
            self.db.rollback()
        spider.logger.error("sucess to write mysql")
        return item

    def open_spider(self, spider):
        """
        called when spider is opened.
        do something before pipeline is processing items.
        example: do settings or create connection to the database.
        """
        try:
            spider.logger.debug("trying to connect mysql")
            self.db = MySQLdb.connect(host=self.mysql_ip, port=self.mysql_port,
                                      user=self.mysql_user,
                                      passwd=self.mysql_password,
                                      db=self.mysql_database,
                                      charset='utf8')
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
        self.db.close()
        return

    @classmethod
    def from_crawler(cls, crawler):
        """
        return an pipeline instance.
        example: initialize pipeline object by crawler's setting and components.
        """
        return cls(crawler.settings.get('MYSQL_IP'),
                   crawler.settings.get('MYSQL_PORT'),
                   crawler.settings.get('MYSQL_NAME'),
                   crawler.settings.get('MYSQL_PASSWORD'),
                   crawler.settings.get('MYSQL_DATABASE'))
