# -*- coding: utf-8 -*-
#import os
#import sys

BOT_NAME = 'wangyi'

#DJANGO_PROJECT_PATH = '../django_spider'
#DJANGO_SETTINGS_MODULE = 'django_spider.settings'

#sys.path.insert(0, DJANGO_PROJECT_PATH)
#os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

SPIDER_MODULES = ['wangyi.spiders']
NEWSPIDER_MODULE = 'wangyi.spiders'

#指定使用scrapy-redis的Scheduler
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#选择去重class
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
SCHEDULER_PERSIST = False

# 指定排序爬取地址时使用的队列，默认是按照优先级排序
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# 可选的先进先出排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# 可选的后进先出排序
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'

DOWNLOAD_TIMEOUT = 300

# 指定RedisPipeline用以在redis中保存item
ITEM_PIPELINES = {
   # 'wangyi.pipelines.News2FileFor163Pipeline': 300,
    'wangyi.pipelines.News2MySQLPipeline': 500,
}

#mysql Master
MYSQL_IP='localhost'
MYSQL_PORT='3306'
MYSQL_NAME='root'
MYSQL_PASSWORD='123456'
MYSQL_DATABASE='python'

# 指定redis的连接参数 Master
# REDIS_PASS是我自己加上的redis连接密码，需要简单修改scrapy-redis的源代码以支持使用密码连接redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


LOG_LEVEL = 'DEBUG'
