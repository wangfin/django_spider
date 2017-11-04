from scrapy import cmdline
from views import TBPara

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


order = 'scrapy crawl taobao'
        #\
        #'-a isTaobao=%s -a isdataSource=%s -a isapiData=%s -a pageres=%s -a resurl=%s -a resurl2=%s -a start_url=%s -a dataurl=%s -a wantpage=%s'\
        #%(isTaobao,isdataSource,isapiData,pageres,resurl,resurl2,start_url,dataurl,wantpage)
#print order
cmdline.execute(order.split())
