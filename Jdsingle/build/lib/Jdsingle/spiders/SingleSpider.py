# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import requests
from scrapy.http import Request
from scrapy.selector import Selector
from Jdsingle.items import JdsingleItem
import re
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')


class SingleSpider(CrawlSpider):
    """继承自CrawlSpider，实现自动爬取的爬虫。"""

    name = "JdSingleSpider"
    # 设置下载延时
    download_delay = 2
    allowed_domains = ['jd.com']
    # 第一篇文章地址



    
    def __init__(self,url=None, *args, **kwargs):
        super(SingleSpider, self).__init__(*args, **kwargs)
        
        # 打开数据库连接
        db = MySQLdb.connect("localhost","root","123456","python",charset='utf8' )

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute("SELECT * from timing_task where name =" + "'"+url+"'")

        # 使用 fetchone() 方法获取一条数据库。
        data = cursor.fetchone()

        self.start = data[2]
        print data[2]
        # url表示第一篇文章的地址
        self.start_urls.append(data[2])
          # 关闭数据库连接
        db.close()

    
    def start_requests(self):
        print u'进入一般商品页'
        singleid = re.search(r'item.jd.com/(\d*?).html',self.start).group(1)
        yield Request(url=self.start, callback=self.parse_item, meta={'product_id': singleid})
    #    #提取“下一篇”链接并执行**处理**


    def parse_item(self, response):
        print response.meta['product_id']
        selector = Selector(response)

        products = JdsingleItem()
        products['product_url'] = response.url
        try:
            products['product_name'] = selector.xpath('//title/text()')[0].extract()
            # products['product_name'] = re.search(r'<title>(.*?)【图片 价格 品牌 报价】',selector.xpath("//text()")[0].extract()).group(1)

        except Exception as e:
            products['product_name'] = selector.xpath('//div[@class="sku-name"]/text()')[0].extract()
        # print products['name']

        products['image_url'] = selector.xpath('//img[@id="spec-img"]/@data-origin')[0].extract()

        # 动态获取商品价格
        priceurl = 'https://p.3.cn/prices/mgets?skuIds=J_'
        products['product_id'] = response.meta['product_id']
        price_response = requests.get(url=priceurl + products['product_id'])
        price_json = price_response.json()
        # print 'this is ',price_json
        products['reallyPrice'] = price_json[0]['p']

        print products['reallyPrice']
        products['originalPrice'] = price_json[0]['m']
        print products['originalPrice']

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
        try:
            category = response.meta['category']
        except:
            html = requests.get(response.url)
            category = re.search(r'cat: \[(.*?)],', html.content).group(1)
        # print u'category is',category
        favourable_url = 'https://cd.jd.com/promotion/v2?skuId=%s&area=1_72_4137_0&cat=%s'

        res_url = favourable_url % (products['product_id'], category.replace(',', '%2c'))
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

        # print products['favourableDesc1']


        # 构造评论数量的url
        comments_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='
        comments_response = requests.get(url=comments_url+products['product_id'])
        price_json = comments_response.json()
        productComments = price_json['CommentsCount']
        products['AllCount'] = productComments[0]['CommentCountStr']
        products['GoodCount'] = productComments[0]['GoodCountStr']
        products['AfterCount'] = productComments[0]['AfterCountStr']
        products['GeneralCount'] = productComments[0]['GeneralCountStr']
        products['PoorCount'] = productComments[0]['PoorCountStr']

        # print u'yield 产品item'

        yield products
