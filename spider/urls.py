# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

# 建立URL 与 函数的响应关系

# 有两种URL配置方法

urlpatterns = [
    url(r'^index/$', views.index),#主页面
    url(r'^show_task/$', views.show_task),#显示任务界面
    url(r'^create_task/$', views.create_task),#创建任务界面
    url(r'^show_timetask/$', views.show_timetask),#显示定时任务界面
    url(r'^create_timetask/$', views.create_timetask),#创建定时任务界面
    url(r'^create/$', views.create),#创建任务的函数
    url(r'^time_create/$', views.time_create),#创建定时任务的函数
    url(r'^show/(?P<task_id>[0-9]+)$', views.show,name='show'),#显示具体任务的函数
    #url(r'^article/(?P<article_id>[0-9]+)$', views.article_page,name='article_page'),
    url(r'^getpage/$', views.getpage),#获取爬取页面的页面总数
    url(r'^show_jd/$', views.show_jd),#获取京东爬虫的任务
    url(r'^show_tb/$', views.show_tb),#获取淘宝爬虫的任务
    url(r'^show_wy/$', views.show_wy),#获取网易爬虫的任务
    url(r'^show_csdn/$', views.show_csdn),#获取CSDN的任务
    url(r'^jd_products/(?P<task_id>[0-9]+)$', views.jd_products,name='jd_products'),#显示具体京东爬虫的数据
    url(r'^tb_products/(?P<task_id>[0-9]+)$', views.tb_products,name='tb_products'),#显示具体淘宝爬虫的数据
    url(r'^wy_news/(?P<task_id>[0-9]+)$', views.wy_news, name='wy_news'),  # 显示具体网易新闻爬虫的数据
    url(r'^csdn_blogs/(?P<task_id>[0-9]+)$', views.csdn_blogs, name='csdn_blogs'),  # 显示具体网易新闻爬虫的数据
    url(r'^stop/$', views.stop),#停止爬虫任务
    url(r'^delete/$', views.delete),#停止爬虫任务
    url(r'^show_graphical/$', views.show_graphical),  # 显示任务图表数据
    url(r'^show_graphical/$', views.show_graphical),  # 显示图表数据
    url(r'^check_cpu/$', views.check_cpu),  # 检查cpu的使用情况
    url(r'^show_calendar/$', views.show_calendar),  # 显示日历
    url(r'^check_mem/$', views.check_mem),  # 检查内存的使用情况
    #url(r'^calendar/$', views.calendar),  # 显示日历
    url(r'^product_list/$', views.product_list),  # 检查内存的使用情况
    url(r'^gettop/$', views.gettop),  # 检查内存的使用情况
    url(r'^getlast/$', views.getlast),  # 检查内存的使用情况
    url(r'^getpricediv/$', views.getpricediv),  # 检查内存的使用情况
    url(r'^product_detail/$', views.product_detail),  # 检查内存的使用情况
    url(r'^getdifferentprice/(.+)/$', views.getdifferentprice, name='getdifferentprice'),  
    url(r'^show_productdetail/(.+)/$', views.show_productdetail, name='show_productdetail'), 
]
