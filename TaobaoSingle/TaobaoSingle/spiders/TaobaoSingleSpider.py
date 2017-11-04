# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from TaobaoSingle.items import TaobaosingleItem
from scrapy.selector import Selector
import sys
import requests
import re
import time
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb


class TaobaoSingel(CrawlSpider):


    name = 'TaobaoSingleSpider'
    # s = raw_input('输入你要爬取的url')

    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def __init__(self,url=None,*args, **kwargs):
        super(TaobaoSingel, self).__init__(*args, **kwargs)
          # 打开数据库连接
        db = MySQLdb.connect("localhost","root","123456","python",charset='utf8' )

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute("SELECT * from timing_task where name =" + "'"+url+"'")

        # 使用 fetchone() 方法获取一条数据库。
        data = cursor.fetchone()

        #self.start = data[2]
        self.start_url = data[2]

    def start_requests(self):
        print u'进入start_request'
        singleid = re.search(r'id=(\d*)',self.start_url).group(1)


        yield Request(url=self.start_url, callback=self.parse_Taobaoproduct,meta={'product_id':singleid})
     

    # 该方法用于通过sellerid和商品id获取商品的评论总数
    def getallcountByid(self, sellerid, id):
        url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s&sellerId=%s' % (id, sellerid)
        html = requests.get(url).content
        return re.search(r'"rateTotal":(\d*),"', html).group(1)

    def getPricefromurl(self, url, id):
        # print 'the priceurl is',url
        # print 'the id is',id
        headers = {
            "cookie": "thw=cn; l=Alpa82K2TT0LI-7Jkcvv-wM8Kg59ut5l; miid=1785193269824995977; v=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dBzWYesWuP8YrIrNw%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; existShop=MTUwNDA4MDY3MA%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=18f8d9ebd59e346eef2eb5f6b6d784a7; skt=99ea9b3b3d5c643f; t=e8823214ea1fe4e93a65b5419a02f29b; _cc_=U%2BGCWk%2F7og%3D%3D; tg=0; mt=ci=29_1; swfstore=297832; whl=-1%260%260%261504142217051; _tb_token_=73b07be1eb779; cna=VGrXDroWdwACAXAZiUThcFIk; uc1=cookie14=UoTcC%2B1i%2BcMf1w%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=W5iHLLyFeYZ1WM9hVnmS&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; linezing_session=KyPSyoxlkXKtokjVGJfqww4d_1504142216944lWk5_4; isg=Atvb7vaXBsW6e3oP4yOGHKKHaj-FGMTvQdKJ2M0Yt1rxrPuOVYB_AvkuMjrZ; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            'authority': 'detailskip.taobao.com',
            'referer': 'https://item.taobao.com/item.htm?id=%s' % id
        }
        s = requests.get(url, headers=headers)
        # print s.content
        try:
            price = re.search(r'"price":"(\d*\.\d*)","start":false', s.content).group(1)
        except:
            try:
                price = re.search(r'"price":"(.*?)","contract', s.content).group(1)
            except:
                price = re.search(r'"price":"(.*?)","tradeContract"', s.content).group(1)

        return price
    
    
    def getDetailCount(self,url):
        data = requests.get(url).content
        counts = []
        counts.append(re.search(r'"total":(.*?),"tryRepor', data).group(1))
        counts.append(re.search(r'"goodFull":(.*?),"additiona', data).group(1))

        counts.append(re.search(r'"normal":(.*?),"hascon', data).group(1))
        counts.append(re.search(r'"bad":(.*?),"totalFull', data).group(1))
        counts.append(re.search(r'"additional":(.*?),"correspo', data).group(1))
        return counts


    def parse_Taobaoproduct(self,response):
        # print 'parse taobao'
        # print u'this is taobao'
        selector = Selector(response)
        # htmltext = requests.get(response.url).content
        item = TaobaosingleItem()
        item['product_name'] = selector.xpath('//div[@id="J_Title"]/h3/text()').extract()[0].replace("\r\n",'').replace(' ','').strip()
        # print 'product_name is',item['product_name']
        item['product_url'] = response.url
        # print 'url is',item['product_url']
        item['product_id'] = response.meta['product_id']
        # print 'product_id is',item['product_id']
        item['Price'] = selector.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()[0]
        # print 'price is ',item['Price']

        image_url = selector.xpath('//img[@id="J_ImgBooth"]/@src').extract()[0]
        item['img_url'] = image_url



        priceurldatas = re.search(r"sib.htm\?(.*?)',",response.body).group(1)
        #构造实际价格的url
        priceurl = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?%s'%priceurldatas
        # print priceurl
        item['ActualPrice'] = self.getPricefromurl(priceurl,item['product_id'])
        # print 'the actual price is',item['ActualPrice']

        # item['sellerid'] = re.search(r'sellerId=(\d*)&modules',priceurldatas).group(1)
        # item['sellerlink'] = re.search(r"url : '(.*?)'",re.search(r"shop  : {(.*?)vdata :{",htmltext).group(1)).group(1)

        shopdata = re.search(r"shop  : {(.*?)vdata", response.body, re.S).group(1)
        item['sellerlink'] = re.search(r"url : '(.*?)'", shopdata).group(1)
        # print item['sellerlink']
         # sellerNick: '梦倩的衣柜'
        item['sellerNick'] = re.search(r"sellerNick       : '(.*?)'",response.body).group(1).decode('gbk')
        # print item['sellerid']
        # print item['sellerNick']

        commenturl = 'https://rate.taobao.com/detailCommon.htm?auctionNumId=%s'%item['product_id']
        detailCount = self.getDetailCount(commenturl)
        # print detailCount
        item['AllCount'] =detailCount[0]
        item['GoodCount'] = detailCount[1]
        item['GeneralCount'] =detailCount[2]
        item['PoorCount'] = detailCount[3]
        item['AfterCount'] = detailCount[4]
        yield item
