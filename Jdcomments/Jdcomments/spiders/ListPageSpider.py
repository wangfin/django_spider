# -*- coding: utf-8 -*-
import redis
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from Jdcomments.items import CategoriesItem
from Jdcomments.items import productsItem
import json
import sys
import requests
import re
import MySQLdb
import time
from Jdcomments.handledb import MysqldbHelper

from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding('utf-8')

# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)


class ListSpider(RedisSpider):
    name = 'jingdongproducts'
    redis_key = 'jingdongproducts:start_urls'
    # start_urls = ['https://list.jd.com/list.html?cat=9987,653,655']


    # allowed_domains = ["jd.com"]  # 允许爬取的域名，非此域名的网页不会爬取

    # 用来保持登录状态，可把chrome上拷贝下来的字符串形式cookie转化成字典形式，粘贴到此处
    cookies = {
        "Cookie": 'user-key=09c4481b-4286-47b9-8de5-1f7e34823fd5; ipLoc-djd=1-72-2799-0; cn=0; unpl=V2_ZzNtbRBRFkZxX0AELklZDGIGRVUSAEJFdghOVS4eDFJjURtVclRCFXMUR1NnGl4UZwsZX0ZcQx1FCHZXfBpaAmEBFl5yAR1LI1USFi9JH1c%2bbUgbF0tGE3IATl1yGVsMVzMRXXJXQiV1DU5SfxtcA2YBG11CVEIQdglOXH8YVDVXBCJtclRDEHUIdlVLGGxHM18aWUFQRRE4CENcfR1eBWECEFRCV0AUcAtHXHMdXQ1XAiJe; __jdv=122270672|google-search|t_262767352_googlesearch|cpc|kwd-4769988168_0_c7db5f7ada4844f9af0a2190d6af5c89|1498217719859; wlfstk_smdl=0eq15yvm1odqct48ujobmbm97qhj9x29; _jrda=1; _jrdb=1498218889349; TrackID=1OhOIyjNDzOAm_E4wK2ib3VLTLALHg9bfEGSEc8Zqt3Xip0p-AMNcTIrgHCd9R_3VbJU39BvRvhagju9k2wP6ea478b2-C1FNoWfxTy6Y4ZQ; pinId=tsR6knRra863ZakWEAEjXLV9-x-f3wj7; pin=jd_545465ea70b5c; unick=%E7%A9%BA%E5%B1%B1%E5%A4%A9%E8%A1%8C; thor=BFCD218DBFC8983D2EE7D5D325EC52300DAB180E3694BBD8B6FF002DB6F047260A9D0BC62237ECD77818B668334BCAC3C5CBCF999F12FF46A283FBFC8A9692D2ADEFF8D9DE421889E1534790A52BD86B94600435000BF368CCF11F88FBB4A98A1975A10AAA2C2DC70E68A429318393C7B678045AD407A65D296F9BFB5D170D46B30F19273F16E1175674A24101B5FAB5772B690A85C437E54BEF3EFE634E9C43; _tp=JKnkV0AJ34uv5cQbvuvul4FiQPTb41kDXXvjFOkiGSI%3D; _pst=jd_545465ea70b5c; ceshi3.com=000; __jda=122270672.14975317038112042099509.1497531703.1498113558.1498217720.16; __jdb=122270672.10.14975317038112042099509|16.1498217720; __jdc=122270672; rkv=V0600; __jdu=14975317038112042099509; 3AB9D23F7A4B3C9B=572XHAHCWHNOQAXBCVIEMO5JVLZGHT7H3RLZ7ZTHHQX2GZE2CRT3U5KTFOPMTUACBVXBJ4ZUJONCA4KSBGBTRBWIOQ; xtest=3037.8543.5882.cf6b6759; mx=0_X'
    }
    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
    pages = 0

    def __init__(self, totalpage=None, flag=None, isurl=None, start_url=None, wantpage=None, *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)
        self.totalpage = r.get('jd_totalpage')
        self.flag = r.get('jd_flag')
        self.isurl = r.get('jd_isurl')
        self.start_url = r.get('jd_url')
        self.start_urls.append(start_url)
        self.wantpage = r.get('jd_wantpage')
        # self.start_requests()

    def get_next_url(self, page, url):
        if page < self.pages:
            #print u'返回的旧的url是', url
            # s = url.split('&')
            # 如果是searchurl
            if re.findall(r'Search', url).__len__() != 0:
                if page == 1:
                    new_url = url + '&page=3'
                else:
                    new_url = url.replace(re.search('page=\d*', url).group(), 'page=%d' % (page + 2))

            # 如果url来自数据库
            else:
                if page == 1:
                    new_url = url + '&page=2'
                else:
                    new_url = url.replace(re.search('page=\d*', url).group(), 'page=%d' % (page + 1))

            return new_url  # 返回新的url
        else:
            return

    def get_next_url2(self, page, url):
        if page < self.pages:
            #print u'返回的旧的url是', url
            if page == 1:
                new_url = url + '&page=3'
            else:
                new_url = url.replace(re.search('page=\d*', url).group(), 'page=%d' % (page + 2))

            return new_url
        else:
            return

    def start_requests(self):
        """
        这是一个重载函数，它的作用是发出第一个Request请求
        :return:
        """
        #print u'这里是装载参数'
        # keyname = raw_input('输入你想要爬取的商品的关键字或者url')

        # 若给定初始url
        # if re.findall(r'/',keyname).__len__()!=0:#由前端页面获取isurl标志判断
        if str(self.isurl) == '1':
            # s = raw_input('1表示单页爬取，2表示多页爬取') #该值在前端直接判断url的类型
            s = self.flag
            if s == '2':
                pageall = self.totalpage  # 该值由getpage文件传递过来
                # wantpage = raw_input('输入你想爬取的页数（不要让人家太累哦~~）')#该值在前端输入由getpage传递过来

                if int(self.wantpage) > pageall:
                    #print u'人家只能爬', pageall, u'页啦'
                    return
                else:
                    self.pages = (int(self.wantpage) * 4) - 1

                yield Request(url=self.start_url, callback=self.parse3, headers=self.headers, cookies=self.cookies,
                              meta=self.meta)
                return
            elif s == '1':
                yield Request(url=self.start_url, callback=self.parse4, headers=self.headers, cookies=self.cookies,
                              meta=self.meta)
                return
            else:
                #print u'你所输入字符不合法'
                return

        # 从数据库中获取url或者自行构造url
        # urls = self.getUrlBySearchname(keyname)
        # print urls#通过参数传递
        elif self.isurl == '2':
            for eachurl in self.start_urls:
                # print eachurl['names'],eachurl['url']
                # html = requests.get(eachurl['url'])
                # print html
                # selector = Selector(html)
                # try:
                #     pageall = selector.xpath('//span[@class="p-skip"]/em/b/text()').extract()[0]#同样由前端获取
                #     # print u'这类商品共有', pageall, u'页'
                # except Exception as e :
                #     print u'该url没有总页数'
                #     pageall = 100
                #     # continue
                # wantpage = raw_input('输入你想爬到的页数（不要让人家太累哦~~）')#通过前端传递
                if int(self.wantpage) > self.totalpage:
                    # print u'人家只能爬',pageall,u'页啦'
                    return
                else:
                    self.pages = int(self.wantpage)
                    if re.findall(r'Search', eachurl).__len__() != 0:
                        yield Request(eachurl, callback=self.parse2, headers=self.headers, cookies=self.cookies,
                                      meta=self.meta)
                    else:
                        yield Request(eachurl, callback=self.parse, headers=self.headers, cookies=self.cookies,
                                      meta=self.meta)

    def getUrlBySearchname(self, keyname):
        # print u'keyname is',keyname

        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='python', port=3306, charset='utf8')
        cur = conn.cursor(MySQLdb.cursors.DictCursor)

        sqlHelper = MysqldbHelper()
        # keyname = '%'+keyname+'%'
        #print keyname
        sql = "select * from jdmenu where names = '%s'" % keyname
        # print sql
        result = sqlHelper.select(sql)
        #print result
        pass

        if result.__len__() == 0:
            result = ({'url': 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % keyname, 'names': keyname},)
            # result[0]['name'] = keyname
            # result[0]['url'] = 'https://search.jd.com/Search?keyword=%s&enc=utf-8'%keyname

        return result

    def parse(self, response):
        """分别获得商品的地址和下一页地址"""
        #print u'进入列表页'
        meta = dict()
        meta['category'] = response.url.split('=')[1].split('&')[0]
        #print meta['category']
        # print u'category is',response.url
        selector = Selector(response)
        texts = selector.xpath('//*[@id="plist"]/ul/li/div/div[@class="p-img"]/a').extract()
        for text in texts:
            items = re.findall(r'<a target="_blank" href="(.*?)">', text)
            product_id = re.search(r'item.jd.com/(.*?).html', text).group(1)
            # print product_id
            #print items[0]
            yield Request(url='https:' + items[0], callback=self.parse_product,
                          meta={'product_id': product_id, 'category': meta['category']})

        if re.search(r'page=(\d*)', str(response.url)) == None:
            pagenum = 1
        else:
            pagenum = int(re.search(r'page=(\d*)', str(response.url)).group(1))

        #print 'pagenum is', pagenum

        next_url = self.get_next_url(pagenum, response.url)
        if next_url != None:  # 如果返回了新的url
            #print next_url
            yield Request(next_url, callback=self.parse, headers=self.headers, cookies=self.cookies, meta=self.meta)
            # NextUrl = selector.xpath('//a[@class="pn-next"]/@href').extract()[0]
            # if NextUrl:
            #     print u'进入NextUrl'
            #     # print requests['proxy']
            #     yield Request(url='https:' + response.url+'&page=2',callback = self.parse)
            # print 'the next url is',NextUrl

    def parse2(self, response):
        #print u'进入列表页2'
        selector = Selector(response)
        texts = selector.xpath('//div[@id="J_goodsList"]/ul/li/div/div[@class="p-img"]/a').extract()
        #print texts
        for text in texts:
            items = re.findall(r'href="(.*?)" onclick', text)
            #print items
            product_id = re.search(r'item.jd.com/(.*?).html', text).group(1)

            yield Request(url='https:' + items[0], callback=self.parse_product, meta={'product_id': product_id})

        # 构造带有页数的url,先获取当前页的页数
        if re.search(r'page=(\d*)', str(response.url)) == None:
            pagenum = 1
        else:
            pagenum = int(re.search(r'page=(\d*)', str(response.url)).group(1))

        #print 'pagenum is', pagenum

        next_url = self.get_next_url(pagenum, response.url)
        if next_url != None:  # 如果返回了新的url
            #print next_url
            yield Request(next_url, callback=self.parse2, headers=self.headers, cookies=self.cookies, meta=self.meta)
        pass

    def parse3(self, response):
        #print u'进入列表页3'
        selector = Selector(response)
        texts = selector.xpath('//div[@id="J_goodsList"]/ul/li/div/div[@class="p-img"]/a').extract()
        #print texts
        for text in texts:
            try:
                items = re.findall(r'href="(.*?)" onclick', text)
                product_id = re.search(r'item.jd.com/(.*?).html', text).group(1)
            except:
                continue
            #print items
            yield Request(url='https:' + items[0], callback=self.parse_product, meta={'product_id': product_id})

        # 构造带有页数的url,先获取当前页的页数
        if re.search(r'page=(\d*)', str(response.url)) == None:
            pagenum = 1
        else:
            pagenum = int(re.search(r'page=(\d*)', str(response.url)).group(1))

        #print 'pagenum is', pagenum

        next_url = self.get_next_url2(pagenum, response.url)
        if next_url != None:  # 如果返回了新的url
            #print next_url
            yield Request(next_url, callback=self.parse3, headers=self.headers, cookies=self.cookies,
                          meta=self.meta)
        pass

    def parse4(self, response):
        #print u'进入一般商品页'
        html = requests.get(response.url)
        allinks_id = re.findall(r'item.jd.com/(\d*?).html', html.content)
        for eachid in allinks_id:
            eachurl = 'http://item.jd.com/' + eachid + '.html'
            product_id = eachid
            #print eachurl
            yield Request(url=eachurl, callback=self.parse_product, meta={'product_id': product_id})

    def parse_product(self, response):

        selector = Selector(response)

        products = productsItem()
        products['product_url'] = response.url
        try:
            products['product_name'] = selector.xpath('//title/text()')[0].extract()
            # products['product_name'] = re.search(r'<title>(.*?)【图片 价格 品牌 报价】',selector.xpath("//text()")[0].extract()).group(1)

        except Exception as e:
            products['product_name'] = selector.xpath('//div[@class="sku-name"]/text()')[0].extract()
        # print products['name']

        # 动态获取商品价格
        priceurl = 'https://p.3.cn/prices/mgets?skuIds=J_'
        products['product_id'] = response.meta['product_id']
        #print 'the priceurl is',priceurl + products['product_id']
        price_response = requests.get(url=priceurl + products['product_id'])
        price_json = price_response.json()
        # print 'this is',price_json
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
        comments_response = requests.get(url=comments_url + products['product_id'])
        price_json = comments_response.json()
        productComments = price_json['CommentsCount']
        products['AllCount'] = productComments[0]['CommentCountStr']
        products['GoodCount'] = productComments[0]['GoodCountStr']
        products['AfterCount'] = productComments[0]['AfterCountStr']
        products['GeneralCount'] = productComments[0]['GeneralCountStr']
        products['PoorCount'] = productComments[0]['PoorCountStr']

        # print u'yield 产品item'

        yield products
