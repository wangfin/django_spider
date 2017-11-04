#!/usr/bin/env python
# -*-encoding:UTF-8-*-
from scrapy.selector import Selector
from wangyi.items import NewsItem
from wangyi.items import DmozItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re
import sys
reload(sys)
sys.setdefaultencoding('gbk')

import requests
from wangyi.handledb import MysqldbHelper

import redis
from scrapy_redis.spiders import RedisSpider
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)

class NewsSpider(RedisSpider):
    """
    spider for tech news.
    """
    # spider name
    name = "technewsspider"
    redis_key = 'technewsspider:start_urls'

    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    # An optional list of strings containing domains that this spider is allowed
    # to crawl.
    # allowed_domains = ["163.com",
    #                    "tech.qq.com",
    #                    "tech.sina.com.cn",
    #                    "tech.ifeng.com",
    #                    "it.sohu.com"]

    # The subsequent URLs will be generated successively from data contained in
    # the start URLs.
    keyname = ''
    num = 0
    def __init__(self, wantnum=None,start_url=None, *args, **kwargs):
        # print category
        super(NewsSpider, self).__init__(*args, **kwargs)
        # self.keyname = category
        # self.start_urls = ['http://%s.163.com' % category]
        # self.start_urls = [ 'http://news.163.com/rank/']

        self.wantnum = r.get('wy_wantpage')
        self.start_urls.append(r.get('wy_url'))




    # start_urls = []
    # start_urls.append('http://news.163.com')

                  # "http://tech.qq.com",
                  # "http://tech.sina.com.cn",
                  # "http://tech.ifeng.com",
                  # "http://it.sohu.com"]

    #  If multiple rules match the same link, the first one will be used,
    #  according to the order they’re defined in this attribute.
    # rules = [
    #     Rule(LinkExtractor(allow='tech.163.com/\d{2}/\d{4}/\d{2}/.*\.html'),
    #          follow=False, callback='parse_item'),
    #     Rule(LinkExtractor(allow='tech.qq.com/a/\d{8}/.*\.htm'),
    #          follow=False, callback='parse_item'),
    #     Rule(LinkExtractor(
    #         allow='tech.sina.com.cn/.*/\d{4}-\d{2}-\d{2}/.*\.shtml'),
    #         follow=False, callback='parse_item'),
    #     Rule(LinkExtractor(allow='tech.ifeng.com/a/\d{8}/.*\.shtml'),
    #          follow=False, callback='parse_item'),
    #     Rule(LinkExtractor(allow='it.sohu.com/\d{8}/.*\.shtml'),
    #          follow=False, callback='parse_item'),
    # ]

    # rules = [
    #     Rule(LinkExtractor(allow="%s.163.com/\d{2}/\d{4}/\d{2}/.*\.html"%keyname),
    #          follow=False, callback='parse_item')]

    # rules = [
    #     Rule(LinkExtractor(allow=".*?.163.com/\d{2}/\d{4}/\d{2}/.*\.html" ),
    #          follow=False, callback='parse_item')]

    # def start_requests(self):
    #
    #     s = raw_input('请输入你想爬取的url')
    #     self.start_urls.append(s)
        # mysqlHelper = MysqldbHelper()
        # sql = "select * from 163menu where title = '%s'"%s
        # result = mysqlHelper.select(sql)





    def parse(self, response):
        """
        parse News item from response.
        """

        item = NewsItem()
        self.logger.debug("start to parse url: %s" % response.url)
        item['url'] = [response.url]
        try:
            if bool(re.match(r'http://.*?.163.com/\d{2}/\d{4}/\d{2}/.*\.html',response.url).group()) == True:
                yield Request(url = response.url,callback=self.parse_item_163)
                return
        except:
            if re.search(r"\.163\.com", response.url) is not None:
                print u'the response url is ',response.url
                # print u'keyname is ',self.keyname
                # return self.getAllCategory(response)
                html = requests.get(response.url)
                properurls = re.findall(r'http://.*?.163.com/\d{2}/\d{4}/\d{2}/.*?\.html',html.content)
                # 去除列表中重复的元素
                properurls2 = list(set(properurls))
                for eachurl in properurls2:
                    print eachurl
                    if(self.num<int(self.wantnum)):
                        print 'the num is ',self.num
                        yield Request(url= eachurl,callback=self.parse_item_163)
                        self.num = self.num + 1
                    else:
                        return

            # return self.parse_item_163(response)
        # if re.search(r"tech\.qq\.com", response.url) is not None:
        #     return self.parse_item_qq(response)
        # if re.search(r"tech\.sina\.com.cn", response.url) is not None:
        #     return self.parse_item_sina(response)
        # if re.search(r"tech\.ifeng\.com", response.url) is not None:
        #     return self.parse_item_ifeng(response)
        # if re.search(r"it\.sohu\.com", response.url) is not None:
        #     return self.parse_item_sohu(response)
        # return item

    def getAllCategory(self,response):
        html = requests.get(response.url)
        selector = Selector(html)
        quicknav = selector.xpath('//div[@class="ntes-quicknav-content"]/ul')
        nav2 = selector.xpath('//div[@class="ns_area list"]/ul/li')
        for eachnav in nav2:
            item = DmozItem()
            try:
                item['title'] = eachnav.xpath('a/text()').extract()[0]
                item['link'] = eachnav.xpath('a/@href').extract()[0]
                print item['title'], item['link']
                yield item
            except Exception as e:
                print e



        print quicknav
        for eachnav in quicknav:
            alldetail = eachnav.xpath('li')
            # print alldetail
            for eachdetail in alldetail:
                item = DmozItem()
                try:
                    item['title'] = eachdetail.xpath('h3/a/text()').extract()[0]
                    item['link'] = eachdetail.xpath('h2/a/@href').extract()[0]
                    print item['title'],item['link']
                    yield item
                except Exception as e:
                    # print e
                    try:

                        item['title'] = eachdetail.xpath('a/text()').extract()[0]
                        item['link'] = eachdetail.xpath('a/@href').extract()[0]
                        yield item
                        print item['title'],item['link']
                    except Exception as e:
                        continue

                # if eachdetail.xpath('h3/a/text()').extract()[0]!=None:
                #     print eachdetail.xpath('h3/a/text()').extract()[0]
                # elif eachdetail.xpath('a/text()').extract()[0]!=None:
                #     print eachdetail.xpath('a/text()').extract()[0]
                # else:
                #     continue



    def parse_item_163(self, response):
        """
        parse 163 News item from response.
        """
        html = requests.get(response.url)

        self.logger.debug("parse func: %s" % sys._getframe().f_code.co_name)
        item = NewsItem()
        item['url'] = [response.url]
        item['id'] = response.url.split('/')[-1].replace('.html','')
        item['source'] =\
            response.xpath('//a[@id="ne_article_source"]/text()').\
            extract()
        if item['source'].__len__()==0:
            item['source'] = response.xpath('//p[@id="psource"]/a/text()').extract()

        item['title'] =\
            response.xpath('//div[@class="post_content_main"]/h1/text()').\
            extract()
        # print u'title is',item['title']
        if item['title'].__len__()==0:
            item['title'] = response.xpath('//h1[@id="h1title"]/text()').extract()
        if item['title'].__len__() == 0:
            item['title'] = response.xpath('//meta[@name="description"]/@content').extract()


        item['editor'] =\
            response.xpath('//span[@class="ep-editor"]/text()').\
            extract()
        if item['editor'].__len__() == 0:
            item['editor'] = ''

        item['time'] =\
            response.xpath('//div[@class="post_time_source"]/text()').\
            extract()
        if item['time'].__len__()==0:
            item['time'] = response.xpath('//div[@class="ep-time-soure cDGray"]/text()').extract()
        if item['time'].__len__() == 0:
            item['time'] = response.xpath('//p[@id="ptime"]/text()').extract()

        item['content'] = response.xpath('//div[@id="endText"]/p/text()').extract()

        for key in item:
            for data in item[key]:
                self.logger.debug("item %s value %s" % (key, data))
        yield item

    def parse_item_qq(self, response):
        self.logger.debug("parse func: %s" % sys._getframe().f_code.co_name)
        item = NewsItem()
        item['url'] = [response.url]
        item['source'] =\
            response.xpath('//span[@class="where"]/text()').extract()
        item['title'] =\
            response.xpath('//div[@class="main"]/div[@id="C-Main-Article-QQ"]'
                           '/div[@class="hd"]/h1/text()').extract()
        item['editor'] =\
            response.xpath('//span[@class="auth"]/text()').extract()
        item['time'] =\
            response.xpath('//span[@class="pubTime"]/text()').extract()
        item['content'] =\
            response.xpath('//div[@id="Cnt-Main-Article-QQ"]'
                           '/p/text()').extract()
        for key in item:
            for data in item[key]:
                self.logger.debug("item %s value %s" % (key, data))
                print ("item %s value %s" % (key, data))
        return item

    def parse_item_sina(self, response):
        self.logger.debug("parse func: %s" % sys._getframe().f_code.co_name)
        item = NewsItem()
        item['url'] = [response.url]
        item['source'] =\
            response.xpath('//div[@class="main_content"]'
                           '//span[@class="source"]/text()').extract()
        item['title'] =\
            response.xpath('//div[@class="main_content"]'
                           '//h1[@id="main_title"]/text()').extract()
        item['editor'] = []
        item['time'] =\
            response.xpath('//div[@class="main_content"]'
                           '//span[@class="titer"]/text()').extract()
        item['content'] =\
            response.xpath('//div[@class="content"]/p/text()').extract()
        for key in item:
            for data in item[key]:
                self.logger.debug("item %s value %s" % (key, data))
                print ("item %s value %s" % (key, data))
        return item

    def parse_item_sohu(self, response):
        self.logger.debug("parse func: %s" % sys._getframe().f_code.co_name)
        item = NewsItem()
        item['url'] = [response.url]
        item['source'] =\
            response.xpath('//div[@class="news-title"]'
                           '//span[@class="writer"]/a/text()').extract()
        item['title'] =\
            response.xpath('//div[@class="news-title"]/h1/text()').extract()
        item['editor'] = []
        item['time'] =\
            response.xpath('//div[@class="news-title"]'
                           '//span[@class="time"]/text()').extract()
        item['content'] =\
            response.xpath('//div[@class="text clear"]'
                           '//p//span/text()').extract()
        for key in item:
            for data in item[key]:
                self.logger.debug("item %s value %s" % (key, data))
                print ("item %s value %s" % (key, data))
        return item

    def parse_item_ifeng(self, response):
        self.logger.debug("parse func: %s" % sys._getframe().f_code.co_name)
        item = NewsItem()
        item['url'] = [response.url]
        item['source'] =\
            response.xpath('//span[@itemprop="publisher"]'
                           '//span/text()').extract()
        item['title'] =\
            response.xpath('//h1[@id="artical_topic"]/text()').extract()
        item['editor'] = []
        item['time'] =\
            response.xpath('//span[@itemprop="datePublished"]/text()').extract()
        item['content'] =\
            response.xpath('//div[@id="main_content"]//p/text()').extract()
        for key in item:
            for data in item[key]:
                self.logger.debug("item %s value %s" % (key, data))
                print ("item %s value %s" % (key, data))
        return item

    def parse_start_url(self, response):
        """
        parse start url responses.
        It allows to parse the initial responses.
        """
        self.logger.debug("do not parse start url")
        # print self.settings.items.()
        return NewsItem()
