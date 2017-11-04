# -*- coding: utf-8 -*-
import redis
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from csdn.items import CsdnItem
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from csdn.pipelines import CsdnPipeline
from scrapy_redis.spiders import RedisSpider

# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)


class CSDNBlogCrawlSpider(CrawlSpider):
    """继承自CrawlSpider，实现自动爬取的爬虫。"""


    
    name = "CSDNBlogCrawlSpider"
    #redis_key = 'CSDNBlogCrawlSpider:start_urls'
    # 设置下载延时
    download_delay = 2
    allowed_domains = ['blog.csdn.net']
    # 第一篇文章地址
    #start = r.get('csdn_url')#raw_input("请输入起始博客的链接")
    # list = start.split('/')
    # str = list[3] + '/' + list[4] + '/' + list[5]
    #start_urls = [start]

    num = 0

    wantnum = r.get('csdn_wantpage')#raw_input("请输入爬取的条数")r.get('jd_flag')
    direct = '1' #raw_input("1表示向上2表示向下爬取")


    def __init__(self,url=None,direct=None,wantnum=None, *args, **kwargs):
        super(CSDNBlogCrawlSpider, self).__init__(*args, **kwargs)

        self.direct = '1'

        self.start_urls.append(r.get('csdn_url'))
        self.wantnum = r.get('csdn_wantpage')
        print r.get('csdn_wantpage')

    # rules编写法一，官方文档方式
    # rules = [
    #    #提取“下一篇”的链接并**跟进**,若不使用restrict_xpaths参数限制，会将页面中所有
    #    #符合allow链接全部抓取
    #    Rule(SgmlLinkExtractor(allow=('/u012150179/article/details'),
    #                          restrict_xpaths=('//li[@class="next_article"]')),
    #         follow=True)
    #
    #    #提取“下一篇”链接并执行**处理**
    #    #Rule(SgmlLinkExtractor(allow=('/u012150179/article/details')),
    #    #     callback='parse_item',
    #    #     follow=False),
    # ]

    # rules编写法二，更推荐的方式（自己测验，使用法一时经常出现爬到中间就finish情况，并且无错误码）
    # rules = [
    #     Rule(SgmlLinkExtractor(allow=(str),
    #                            restrict_xpaths=('//li[@class="prev_article"]')),
    #          callback='parse_item',
    #          follow=True),
    #     Rule(SgmlLinkExtractor(allow=(str),
    #                            restrict_xpaths=('//li[@class="next_article"]')),
    #          callback='parse_item',
    #          follow=True)
    # ]


    def parse(self, response):

        # wantnum = CsdnPipeline.wantnum
        # num = CsdnPipeline.num
        # print 'the num is ',num
        # print 'the wantnum is ',wantnum
        # print "parse_item>>>>>>"
        print '进入爬虫'
        item = CsdnItem()
        sel = Selector(response)
        blog_url = str(response.url)
        blog_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()
        # print u'',blog_name[0].replace("\r\n",'').replace(" ",''),''
        item['blog_viewnum'] = sel.xpath('//span[@class="link_view"]/text()').extract()[0]
        item['blog_time'] = sel.xpath('//span[@class="link_postdate"]/text()').extract()[0]
        item['blog_author'] = sel.xpath('//div[@id="blog_title"]/h2/a/text()').extract()[0]
        item['blog_comment'] = ''
        alltext = sel.xpath('//span[@class="link_comments"]//text()').extract()


        for eacht in sel.xpath('//span[@class="link_comments"]//text()').extract():

            item['blog_comment'] = item['blog_comment'] + eacht
    
        # print u'',item['blog_viewnum'],''
        item['blog_title'] = blog_name[0].replace("\r\n",'').replace(" ",'')

        item['blog_content'] = ''
        alltext = sel.xpath('//div[@id="article_content"]//text()').extract()

        # for eachtext in alltext:
        #     item['blog_content'] = item['blog_content'] + eachtext.replace("\r\n",'').replace(' ','')


        for i in range(0, alltext.__len__()-1):

            onetext = alltext[i].replace("\r\n", '').replace(' ', '')
            if '$(function()' in onetext:
                print u'找到你啦'
                continue
            onetext = onetext.replace("'", "\\\'")

            onetext = onetext.replace('"', '\\\"')
            item['blog_content'] = item['blog_content'] + onetext

        print item['blog_content']

        item['blog_picture'] = []
        allimgurl = sel.xpath('//div[@id="article_content"]//img/@src').extract()
        # print allimgurl
        # for eachurl in allimgurl:
        #     # print type(eachurl)
        #     item['blog_picture'] = item['blog_picture'].append(eachurl)
        item['blog_picture'] = allimgurl
        
        num = 0
        item['blog_url'] = blog_url.encode('utf-8')

        yield item

        preurl = sel.xpath('//ul[@class="article_next_prev"]/li[@class="prev_article"]/a/@href').extract()
        print preurl
        nexturl = sel.xpath('//ul[@class="article_next_prev"]/li[@class="next_article"]/a/@href').extract()
        print nexturl
        if(self.num<int(self.wantnum)):
            if(self.direct=='1'):
                if(preurl.__len__()!=0):
                    self.num = self.num +1
                    yield Request(url=preurl[0], callback=self.parse)
            elif(self.direct == '2'):
                if (nexturl.__len__() != 0):
                    self.num = self.num + 1
                    yield Request(url=nexturl[0], callback=self.parse)
            else:
                print u'您输入的字符不合法'
                return


        
