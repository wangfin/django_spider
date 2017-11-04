# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import os

import redis
from pybloom import BloomFilter
import hashlib
from scrapy.exceptions import CloseSpider

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)

class CsdnPipeline(object):
    # num = 0
    # wantnum = raw_input("请输入爬取的条数")
    def __init__(self):

        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
        self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.brandName = 'mybloom'


    def open_spider(self, spider):
        brandName = 'mybloom'
        isexists = os.path.exists(brandName + '.blm')
        if isexists == True:
            self.bf = BloomFilter.fromfile(open(brandName + '.blm', 'rb'))
        else:
            self.bf = BloomFilter(100000, 0.001)


    def process_item(self, item,spider):

        taskid = r.get('csdn_taskid')
        # if(int(self.wantnum)>self.num):
        if spider.name == 'CSDNBlogCrawlSpider':

            blog_title = item['blog_title'].strip()
            blog_author = item['blog_author']
            blog_time = item['blog_time']
            blog_content = item['blog_content'].strip()
            blog_viewnum = item['blog_viewnum']
            blog_comment = item['blog_comment']
            blog_url = item['blog_url']
            blog_picture = item['blog_picture']

            text = blog_content  # codecs.open('../test/doc/02.txt', 'r', 'utf-8').read()
            tr4w = TextRank4Keyword()

            tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

            keywords = ""
            phrases = ""
            summary = ""
            # print('关键词：')
            for item in tr4w.get_keywords(10, word_min_len=1):
                keywords = keywords + item.word + ","  # print(item.word, item.weight)

            # print()
            # print('关键短语：')
            for phrase in tr4w.get_keyphrases(keywords_num=10, min_occur_num=2):
                phrases = phrases + phrase + ","  # print(phrase)

            tr4s = TextRank4Sentence()
            tr4s.analyze(text=text, lower=True, source='all_filters')

            # print()
            # print('摘要：')
            for item in tr4s.get_key_sentences(num=3):
                summary = summary + item.sentence + ","  # print(item.index, item.weight, item.sentence)

            try:
                token = blog_url
                m = hashlib.md5()
                m.update(token)
                encodeStr = m.hexdigest()
                flag = self.bf.add(encodeStr)
                # 当前item没有在bloomfilter中，便将其收集下来，视为增量
                if flag == False:
                    sql = "insert into csdn (taskid,title,author,time,content,viewnum,comment,url,keywords,phrases,summary) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        taskid,blog_title,blog_author,blog_time,blog_content,blog_viewnum,blog_comment,blog_url,keywords,phrases,summary)

                    self.cur.execute(sql)

                    # print 'the num is',self.num
                    self.conn.commit()
                    # print '插入文件'
                    # f = open('info.txt', 'a')
                    # f.writelines('name:' + url + '\n')
                    # f.writelines('url:' + reallyPrice + '\n')
                return item

            except Exception as e:
                print('error:', e)
                self.conn.rollback()
        # else:
        #     raise CloseSpider('close')
        #



    def close_spider(self, spider):
        """
        called when spider is closed.
        do something after pipeline processing all items.
        example: close the database.
        """
        spider.logger.debug("close mysql")
        self.cur.close()
        self.conn.close()
        self.bf.tofile(open('mybloom' + '.blm', 'wb'))
        return
