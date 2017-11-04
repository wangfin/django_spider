from scrapy import cmdline

# 从前端页面的文件获取参数
url = ''
direct = '2'
wantnum = 5

order = 'scrapy crawl CSDNBlogCrawlSpider'
# 传递到spider文件中
order = 'scrapy crawl CSDNBlogCrawlSpider -a url=%s -a direct=%s -a wantnum=%s'%(url,direct,wantnum)
cmdline.execute(order.split())