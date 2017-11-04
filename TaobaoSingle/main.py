# -*- coding: utf-8 -*-
from scrapy import cmdline

# start_url = TBPara.url
# isTaobao = TBPara.isTaobao
# isapiData = TBPara.isapiData
# isdataSource = TBPara.isdataSource
# pageres = TBPara.pageres
# resurl = TBPara.resurl
# resurl2 = TBPara.resurl2
# dataurl = TBPara.dataurl
# wantpage = TBPara.wantpage
# -a pageres=%s -a resurl=%s -a resurl2=%s
# ,pageres,resurl,resurl2

url = raw_input("请输入淘宝商品链接")

order = 'scrapy crawl TaobaoSingleSpider ' \
        '-a url=%s'\
        %(url)

cmdline.execute(order.split())
