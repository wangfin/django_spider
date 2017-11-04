# -*- coding: utf-8 -*-
from scrapy import cmdline

# url从前端传入
url = raw_input("输入连接")
order = 'scrapy crawl JdSingleSpider -a url=%s'%(url)
cmdline.execute(order.split())