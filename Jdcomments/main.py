from scrapy import cmdline
import os
import sys

#sys.path.append('..')
#from search.views import Para

#totalpage = Para.totalpage
#flag = Para.flag
#isurl = Para.isurl
#start_url = Para.url
#wantpage = Para.wantpage

#order = 'scrapy crawl jingdongproducts -a totalpage=%s -a flag=%s -a isurl=%s -a start_url=%s -a wantpage=%s'%(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#order = 'scrapy crawl jingdongproducts -a totalpage=100 -a flag=2 -a isurl=1 -a start_url=https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=129bf332624d41fe90fac16f57b3ceaa -a wantpage=25'
order = 'scrapy crawl jingdongproducts'
cmdline.execute(order.split())