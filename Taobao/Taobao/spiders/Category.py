# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from Taobao.items import TaobaoProductItem
from Taobao.items import TaobaoItem
from Taobao.items import DetailCategoryItem
import json
import sys
import requests
import re
import time

reload(sys)
sys.setdefaultencoding('utf-8')


# class Category(CrawlSpider):
#
#     name = 'taobaoCategory'
#
#     start_urls = ['https://www.taobao.com/tbhome/page/market-list']
#     print start_urls
#
#     def parse(self, response):
#         selector = Selector(response)
#         # try:
#         # text1 = selector.xpath('//ul[@class="category-list"]')
#
#         # 获取大的分类页
#         # for eachtext in text1:
#         #     texts = eachtext.xpath('li[@class="category-list-item "]')
#         #     texts2 = eachtext.xpath('li[@class="category-list-item no-margin-left"]')
#         #     alltexts = texts + texts2
#         #     print alltexts.__len__()
#         #     # print texts + texts2
#         #     for text in alltexts:
#         #         categotyItem = TaobaoItem()
#         #
#         #         categotyItem['name'] = text.xpath('a[@class="category-name"]/text()').extract()[0]
#         #         categotyItem['url'] = text.xpath('a[@class="category-name"]/@href').extract()[0]
#         #         yield categotyItem
#         # except Exception as e:
#         #     print('error:', e)
#
#         # 获取小的分类页
#         alllenth = 0
#         detaillist = selector.xpath('//div[@class="category-items"]')
#         # print detaillist.__len__()
#
#         for eachdetail in detaillist:
#             everydetail = eachdetail.xpath('a[@class="category-name"]')
#             # print everydetail
#             lenth = everydetail.__len__()
#             alllenth = alllenth + lenth
#             print everydetail.__len__()
#             for each in everydetail:
#                 detailItem = DetailCategoryItem()
#                 # print each.xpath('text()').__len__()
#                 if each.xpath('text()').__len__() == 1:
#                     detailItem['name'] = each.xpath('text()').extract()[0]
#                     detailItem['url'] = each.xpath('@href').extract()[0]
#                     yield detailItem
#         print u'共有', alllenth, u'条分类'

