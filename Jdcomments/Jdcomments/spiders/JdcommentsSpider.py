# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from Jdcomments.items import CategoriesItem
from Jdcomments.items import productsItem
from Jdcomments.spiders.ListPageSpider import ListSpider
import json
import sys
import requests
import re
import time
import MySQLdb
from Jdcomments.handledb import MysqldbHelper
reload(sys)
sys.setdefaultencoding('utf-8')

class jdSpider(CrawlSpider):
    name = 'jingdongcat'
    start_urls = ['https://www.jd.com/allSort.aspx']


    def parse(self, response):
        """获取分类页"""
        # selector = Selector(response)
        # list = ListSpider('list')
        # try:
        #     texts = selector.xpath(
        #         '//div[@class="category-item m"]/div[@class="mc"]/div[@class="items"]/dl/dd/a').extract()
        #     keyword = 'list'
        #     for text in texts:
        #         items = re.findall(r'<a href="(.*?)" target="_blank">(.*?)</a>', text)
        #         for item in items:
        #             # print item[0].split('.')[0][2:]
        #             if item[0].split('.')[0][2:] in keyword:
        #                 if item[0].split('.')[0][2:] != 'list':
        #                     yield Request(url='https:' + item[0], callback=self.parse())
        #                 else:
        #                     categoriesItem = CategoriesItem()
        #                     categoriesItem['name'] = item[1]
        #                     categoriesItem['url'] = 'https:' + item[0]
        #                     categoriesItem['_id'] = item[0].split('=')[1].split('&')[0]
        #                     print u'yield 分类item'
        #                     print 'the url is',item[0]
        #                     yield categoriesItem
        #
        #                     # yield Request(url='https:' + item[0], callback=list.parse)
        # except Exception as e:
        #     print('error:', e)
        keyname = raw_input('请输入你想要爬去的商品或者url')
        self.getUrlBySearchname(keyname)


    def getUrlBySearchname(self,keyname):
        # print u'keyname is',keyname
        list = ListSpider(CrawlSpider)

        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='python', port=3306, charset='utf8')
        cur = conn.cursor(MySQLdb.cursors.DictCursor)

        sqlHelper = MysqldbHelper()
        keyname = '%'+keyname+'%'
        print keyname
        sql = "select url from jdmenu where names LIKE '%s'" %keyname
        # print sql
        result = sqlHelper.select(sql)
        print result.__len__()
        for eachresult in result:
            # print u'request 执行'
            print eachresult['url']

            list.get_url_from_data(eachresult['url'])
            # try:
            #     # yield Request(url = eachresult['url'],callback=list.get_url_from_data)
            # except Exception as e:
            #     print 'error is ',e



    def parse_list(self, response):
        """分别获得商品的地址和下一页地址"""
        meta = dict()
        meta['category'] = response.url.split('=')[1].split('&')[0]
        # print meta

        selector = Selector(response)
        texts = selector.xpath('//*[@id="plist"]/ul/li/div/div[@class="p-img"]/a').extract()
        for text in texts:
            items = re.findall(r'<a target="_blank" href="(.*?)">', text)
            product_id = re.search(r'item.jd.com/(.*?).html',text).group(1)
            # print product_id

            yield Request(url='https:' + items[0], callback=self.parse_product, meta = {'product_id':product_id,'category':meta['category']})

    def parse_product(self,response):

        products = productsItem()

        #动态获取商品价格
        priceurl = 'https://p.3.cn/prices/mgets?skuIds=J_'
        products['_id'] = response.meta['product_id']
        price_response = requests.get(url=priceurl + products['_id'])
        price_json = price_response.json()
        products['reallyPrice'] = price_json[0]['p']
        products['originalPrice'] = price_json[0]['m']

        # ids = re.findall(r"venderId:(.*?),\s.*?shopId:'(.*?)'", response.text)
        # if not ids:
        #     ids = re.findall(r"venderId:(.*?),\s.*?shopId:(.*?),", response.text)
        # vender_id = ids[0][0]
        # shop_id = ids[0][1]
        # vender_id = re.search(r'venderId:(.*?),',response.text).group(1)
        # shop_id = re.search(r"shopId:'(.*?)',",response.text).group(1)
        # print 'vender_id is',vender_id
        # print 'shop_id is',shop_id

        # 构造优惠的动态url
        category = response.meta['category']
        favourable_url = 'https://cd.jd.com/promotion/v2?skuId=%s&area=1_72_4137_0&cat=%s'

        res_url = favourable_url % (products['_id'], category.replace(',', '%2c'))
        # print(res_url)
        response = requests.get(res_url)
        fav_data = response.json()
        if fav_data['skuCoupon']:
            desc1 = []
            for item in fav_data['skuCoupon']:
                start_time = item['beginTime']
                end_time = item['endTime']
                time_dec = item['timeDesc']
                fav_price = item['quota']
                fav_count = item['discount']
                fav_time = item['addDays']
                desc1.append(u'有效期%s至%s,满%s减%s' % (start_time, end_time, fav_price, fav_count))
            products['favourableDesc1'] = ';'.join(desc1)

        elif fav_data['prom'] and fav_data['prom']['pickOneTag']:
            desc2 = []
            for item in fav_data['prom']['pickOneTag']:
                desc2.append(item['content'])
            products['favourableDesc1'] = ';'.join(desc2)
        else:
            products['favourableDesc1'] = u'没有优惠'

        print products['favourableDesc1']


        #构造评论数量的url
        comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='
        comments_response = requests.get(url = comments_url+products['_id'])
        price_json = comments_response.json()
        productComments = price_json['CommentsCount']
        products['AllCount'] = productComments[0]['CommentCountStr']
        products['GoodCount'] = productComments[0]['GoodCountStr']
        products['AfterCount'] = productComments[0]['AfterCountStr']
        products['GeneralCount'] = productComments[0]['GeneralCountStr']
        products['PoorCount'] = productComments[0]['PoorCountStr']

        yield products

        # print u'好评',products['AllCount']











