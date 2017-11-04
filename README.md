# django_spider
第六届中软杯：分布式爬虫，前端页面使用bootstrap的后台管理样式，python的django框架，爬虫使用python的scrapy
1. 前端页面使用bootstrap框架
2. 后台使用python的django框架
3. 爬虫项目使用scrapy框架
4. 分布式系统使用scrapy-redis，使用redis队列实现
---
交互说明如下：
后台与scrapy的爬虫交互控制，是通过scrapyd实现，将所有的爬虫提交到scrapyd上，再在网站后台通过http命令实现控制
