# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import redis
import json
import re

from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render

from .models import Task
from .models import CpuUsage
from .models import TimingTask
from . import models
from getjdpage import getJDPage
from gettbpage import getTBPage
from priority import Priority
from time_priority import TimingPriority
from JDspider import JDspider
from TBspider import TBspider
from WYspider import WYspider
from CSDNspider import CSDNspider
from checkcpu import CPU
from timing_check import Timing_check
from django.db import connection, transaction

jdspider = JDspider()
tbspider = TBspider()
wyspider = WYspider()
csdnspider = CSDNspider()
checkcpu = CPU()
timing_check = Timing_check()


# Create your views here.
def index(request):
    #news = models.News.objects.all()
    return render(request,'spider/index.html')

#创建普通爬取任务
def create_task(request):
    return render(request,'spider/create_task.html')

#查看普通任务
def show_task(request):
    tasks = models.Task.objects.all()
    ta = list(tasks)
    for i in range(len(ta)):
        if ta[i].runtype != 'denying':
            jdspider.check(ta[i].jobid)
            tbspider.check(ta[i].jobid)
            wyspider.check(ta[i].jobid)
            csdnspider.check(ta[i].jobid)
    return render(request, 'spider/show_task.html', {'tasks': tasks})
    #return render(request,'spider/show_task.html')

#创建定时任务
def create_timetask(request):
    return render(request,'spider/create_timetask.html')

#查看定时任务
def show_timetask(request):
    tasks = models.TimingTask.objects.all()
    ta = list(tasks)
    for i in range(len(ta)):
        timing_check.check(ta[i].name)
             
    return render(request, 'spider/show_timetask.html', {'tasks': tasks})
    #return render(request,'spider/show_task.html')

# 京东
class JDPara(object):
    # 获取参数
    wantpage = None
    totalpage = None
    flag = None
    isurl = None
    url = None


# 淘宝
class TBPara(object):
    # 获取参数
    isTaobao = None
    isdataSource = None
    isapiData = None
    pageres = None
    resurl = None
    resurl2 = None
    url = None
    dataurl = None
    wantpage = None

# 该类是为了获取爬取深度的页数
# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)

#获取页数
def getpage(request):
    ctx = {}

    #获取页数
    getjdpage = getJDPage()
    gettbpage = getTBPage()

    if request.method == 'POST':
        ctx['url'] = request.POST['url']
        ctx['type'] = request.POST['type']

    if(ctx['type']=="jd"):
        # 获取结果
        back = getjdpage.get_totalpage(ctx['url'])

        JDPara.flag = back['flag']
        JDPara.url = back['url']
        JDPara.isurl = back['isurl']
        JDPara.totalpage = back['totalpage']

    if(ctx['type']=="tb"):
        # 获取结果
        back = gettbpage.start(ctx['url'])

        TBPara.isTaobao = back['isTaobao']
        TBPara.isdataSource = back['isdataSource']
        TBPara.isapiData = back['isapiData']
        TBPara.pageres = back['pageres']
        TBPara.resurl = back['resurl']
        TBPara.resurl2 = back['resurl2']
        TBPara.url = back['url']
        TBPara.dataurl = back['dataurl']

    if(ctx['type']=="wy"):
        back = {"result":"wy_news"}

    if (ctx['type'] == "csdn"):
        back = {"result": "csdn_blog"}

    return JsonResponse(back)

#创建任务
def create(request):
    ctx = {}

    if request.method == 'POST':
        ctx['name'] = request.POST['name']
        ctx['url'] = request.POST['url']
        ctx['type'] = request.POST['type']
        ctx['time'] = request.POST['time']
        ctx['depth'] = request.POST['depth']
        ctx['process'] = 0
        ctx['host'] = request.POST['host']
        ctx['priority'] = request.POST['priority']
        ctx['mysql'] = request.POST['mysql']
        ctx['redis'] = request.POST['redis']

    if (ctx['type'] == "jd"):#京东
        #r.set('jd_taskname',ctx['name'])
        r.set('jd_totalpage', JDPara.totalpage)
        r.set('jd_flag', JDPara.flag)
        r.set('jd_isurl', JDPara.isurl)
        r.set('jd_url', JDPara.url)
        r.set('jd_wantpage', ctx['depth'])

    if (ctx['type'] == "tb"):#淘宝
        #r.set('tb_taskname',ctx['name'])
        r.set('tb_isTaobao', TBPara.isTaobao)
        r.set('tb_isdataSource', TBPara.isdataSource)
        r.set('tb_isapiData', TBPara.isapiData)
        r.set('tb_pageres', TBPara.pageres)
        r.set('tb_resurl', TBPara.resurl)
        r.set('tb_resurl2', TBPara.resurl2)
        r.set('tb_url', TBPara.url)
        r.set('tb_dataurl', TBPara.dataurl)
        r.set('tb_wantpage', ctx['depth'])

    if(ctx['type']=="wy"):#网易新闻
        #Para.c = ctx['blog_url']
        r.set('wy_url', ctx['url'])
        r.lpush('technewsspider:start_urls', ctx['url'])
        r.set('wy_wantpage', ctx['depth'])


    if (ctx['type'] == "csdn"):  # 网易新闻
        # Para.c = ctx['blog_url']
        r.set('csdn_url', ctx['url'])
        r.lpush('CSDNBlogCrawlSpider:start_urls', ctx['url'])
        r.set('csdn_wantpage',ctx['depth'])

        #r.set('wy_taskname',ctx['name'])


    #print ctx['time']

    # 计算优先级，同时对爬虫进行判断是否开启
    pri = Priority()
    level = pri.calculate(ctx['name'], ctx['type'], ctx['priority'], ctx['time'], ctx['depth'])

    #存入mysql数据库
    task = Task.objects.get(name=ctx['name'])  # 查询该条记录，任务名称不能重复
    task.url = ctx['url']  # 修改
    task.type = ctx['type']
    task.time = ctx['time']
    task.depth = ctx['depth']
    task.process = ctx['process']
    task.host = ctx['host']
    task.priority = ctx['priority']
    task.mysql = ctx['mysql']
    task.redis = ctx['redis']
    task.level = level

    task.save()  # 保存
    #obj = models.Task(name=ctx['name'], url=ctx['url'],type=ctx['type'],time=ctx['time'],depth=ctx['depth'],
    #process=ctx['process'],priority=ctx['priority'],mysql=ctx['mysql'],redis=ctx['redis'],level=level)



    back = {'result': '任务创建成功'}

    return JsonResponse(back)

#创建定时任务
def time_create(request):
    ctx = {}

    if request.method == 'POST':
        ctx['name'] = request.POST['name']
        ctx['url'] = request.POST['url']
        ctx['type'] = request.POST['type']
        ctx['time'] = request.POST['time']
        ctx['start_time'] = request.POST['start_time']
        ctx['end_time'] = request.POST['end_time']
        ctx['timing_number'] = request.POST['timing_number']
        ctx['timing_type'] = request.POST['timing_type']
        ctx['host'] = request.POST['host']
        ctx['priority'] = request.POST['priority']
        ctx['mysql'] = request.POST['mysql']
        ctx['redis'] = request.POST['redis']

    
        #obj = models.Task(name=ctx['name'], ctx['url'], ctx['type'],ctx['time'],ctx['timing_number'],ctx['timing_type'],ctx['depth'],ctx['process'],ctx['host'],ctx['priority'],ctx['mysql'],ctx['redis'])
        #obj.save()
          #计算优先级，同时对爬虫进行判断是否开启
        time_priority = TimingPriority()
        level = time_priority.calculate(ctx['name'], ctx['type'], ctx['priority'], ctx['time'], ctx['timing_number'],ctx['timing_type'],ctx['url'],ctx['start_time'],ctx['end_time'])

          #存入mysql数据库
        task = TimingTask.objects.get(name=ctx['name'])  # 查询该条记录，任务名称不能重复
        #task.url = ctx['url']  # 修改
        task.type = ctx['type']
        task.time = ctx['time']
        task.start_minutes = ctx['start_time']
        task.end_minutes = ctx['end_time']
        task.timing_number = ctx['timing_number']
        task.timing_type = ctx['timing_type']
        task.host = ctx['host']
        task.priority = ctx['priority']
        task.mysql = ctx['mysql']
        task.redis = ctx['redis']
        task.level = level

        task.save()  # 保存
    

    back = {'result': '任务创建成功'}

    return JsonResponse(back)

#显示任务具体页面
def show(request,task_id):
    info = models.Task.objects.get(id=task_id)
    return render(request, 'spider/show.html',{'info': info})

#显示京东的爬虫页面
def show_jd(request):
    tasks_all = models.Task.objects.all()
    ta = list(tasks_all)
    for i in range(len(ta)):
        if ta[i].type == 'jd' and ta[i].runtype != 'denying':
            jdspider.check(ta[i].jobid)
    tasks = models.Task.objects.filter(type='jd')

    return render(request, 'spider/jd_task.html',{'tasks': tasks})

#显示京东爬虫数据界面
def jd_products(request,task_id):
    info = models.Jdproducts.objects.filter(taskid=task_id)
    return render(request, 'spider/jd_products.html',{'info': info})

#显示淘宝的爬虫页面
def show_tb(request):
    tasks_all = models.Task.objects.all()
    ta = list(tasks_all)
    for i in range(len(ta)):
        if ta[i].type == 'tb'and ta[i].runtype != 'denying':
            tbspider.check(ta[i].jobid)
    tasks = models.Task.objects.filter(type='tb')
    return render(request, 'spider/tb_task.html',{'tasks': tasks})

#显示淘宝爬虫数据界面
def tb_products(request,task_id):
    info = models.Taobaoproduct.objects.filter(taskid=task_id)
    return render(request, 'spider/tb_products.html',{'info': info})


#显示网易的爬虫页面
def show_wy(request):
    tasks_all = models.Task.objects.all()
    ta = list(tasks_all)
    for i in range(len(ta)):
        if ta[i].type == 'wy' and ta[i].runtype != 'denying':
            wyspider.check(ta[i].jobid)
    tasks = models.Task.objects.filter(type='wy')
    return render(request, 'spider/wy_task.html',{'tasks': tasks})

#显示网易新闻爬虫数据界面
def wy_news(request,task_id):
    #info = serializers.serialize("json", models.News.objects.filter(taskid=task_id))
    info = models.News.objects.filter(taskid=task_id)
    return render(request, 'spider/wy_news.html',{'info': info}) #json.dumps(info)})

#显示csdn的爬虫页面
def show_csdn(request):
    tasks_all = models.Task.objects.all()
    ta = list(tasks_all)
    for i in range(len(ta)):
        if ta[i].type == 'csdn' and ta[i].runtype != 'denying':
            csdnspider.check(ta[i].jobid)
    tasks = models.Task.objects.filter(type='csdn')
    return render(request, 'spider/csdn_task.html',{'tasks': tasks})

#显示CSDN爬虫数据界面
def csdn_blogs(request,task_id):
    info = models.Csdn.objects.filter(taskid=task_id)
    return render(request, 'spider/csdn_blog.html',{'info': info}) #json.dumps(info)})


#显示图表数据页面
def show_graphical(request):
    tasks = models.Task.objects.all()
    return render(request, 'spider/graphical_show.html', {'tasks': tasks} )
    
#检查cpu使用情况
def check_cpu(request):
    checkcpu.MainCheck()
    #cpus = models.CpuUsage.objects.all()
    length = models.CpuUsage.objects.all().count()
    length1 = length - 2
    #cpus = models.CpuUsage.objects.all()[length1:length]
    cpus = serializers.serialize("json", models.CpuUsage.objects.all()[length1:length])
    return HttpResponse(cpus)
    #return render(request, 'spider/graphical_show.html'calendar, {'cpus': cpus} )

#检查内存使用情况
def check_mem(request):
    #checkcpu.MainCheck()
    #cpus = models.CpuUsage.objects.all()
    length = models.MemUsage.objects.all().count()
    length1 = length - 2
    #cpus = models.CpuUsage.objects.all()[length1:length]
    mems = serializers.serialize("json", models.MemUsage.objects.all()[length1:length])
    return HttpResponse(mems)

def show_calendar(request):
    tasks = models.Task.objects.all()
    return render(request, 'spider/calendar.html',{'tasks': tasks})

def product_list(request):
    return render(request, 'spider/product_list.html')

def product_detail(request):
    tasks = models.TimingTask.objects.filter(type='jd_products')
    return render(request, 'spider/product_detail.html', {'tasks': tasks} )

#def calendar(request):
    #tasks = models.Task.objects.all()
    #tasks = serializers.serialize("json", models.Task.objects.all())
    #return render(request, 'spider/calendar.html',{'tasks': tasks})
    #return HttpResponse(tasks)

def gettop(request):

    cursor = connection.cursor()

    # 数据检索操作,不需要提交
    cursor.execute("select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) limit 0,5")
    result = cursor.fetchall()
    name1 = re.search(u'【(.*?)】',result[0][2]).group(1)
    name2 = re.search(u'【(.*?)】',result[1][2]).group(1)
    name3 = re.search(u'【(.*?)】',result[2][2]).group(1)
    name4 = re.search(u'【(.*?)】',result[3][2]).group(1)
    name5 = re.search(u'【(.*?)】',result[4][2]).group(1)


    back = {'name1': name1,'name2': name2,'name3': name3,'name4': name4,'name5': name5,'pri1':result[0][5],'pri2':result[1][5],'pri3':result[2][5],'pri4':result[3][5],'pri5':result[4][5]}
    
    return JsonResponse(back)
    
def getlast(request):

    cursor = connection.cursor()

    # 数据检索操作,不需要提交
    cursor.execute("select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) DESC limit 0,5")
    result = cursor.fetchall()
    name1 = re.search(u'【(.*?)】',result[0][2]).group(1)
    name2 = re.search(u'【(.*?)】',result[1][2]).group(1)
    name3 = re.search(u'【(.*?)】',result[2][2]).group(1)
    name4 = re.search(u'【(.*?)】',result[3][2]).group(1)
    name5 = re.search(u'【(.*?)】',result[4][2]).group(1)

    cursor1 = connection.cursor()


    back = {'name1': name1,'name2': name2,'name3': name3,'name4': name4,'name5': name5,'pri1':result[0][5],'pri2':result[1][5],'pri3':result[2][5],'pri4':result[3][5],'pri5':result[4][5]}
    
    return JsonResponse(back)

def getpricediv(request):
    cursor = connection.cursor()
    cursor.execute("select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) limit 0,1")
    result = cursor.fetchall()
    min = float(result[0][5])
    # print min

    cursor.execute("select count(*) from jdproducts")
    num = cursor.fetchone()
    num = num[0]
    # print num

    cursor.execute("select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) DESC limit 0,1")
    result2 = cursor.fetchall()
    max = float(result2[0][5])
    # print max

    cha = float(max) - float(min)
    if(cha>1000):
        div = round(cha/3,0)
        div1 = min + div
        div1 = round(div1/100,0)*100
        div2 = div1 + div
        div2 = round(div2/100,0)*100
    elif(cha<1000):
        div = round(cha / 3, 0)
        div1 = min + div
        div1 = round(div1 / 10, 0) * 10
        div2 = div1 + div
        div2 = round(div2 / 10, 0) * 10


    cursor.execute("select count(*) from jdproducts where reallyPrice >= %s and reallyPrice <=%s"%(min,div1))
    div1num = cursor.fetchone()
    div1num = div1num[0]
    # print div1num
    perdiv1 = round(div1num*100/num,3)
    # print perdiv1

    s = ''+str(min) + '--'+str(div1)
    strperdiv1 = str(perdiv1)
    dict = {s:strperdiv1}
    # print dict

    cursor.execute("select count(*) from jdproducts where reallyPrice >= %s and reallyPrice <=%s" % (div1, div2))
    div2num = cursor.fetchone()
    div2num = div2num[0]
    # print div2num
    perdiv2 = round(div2num * 100 / num, 3)

    s2 = '' + str(div1) + '--' + str(div2)
    strperdiv2 = str(perdiv2)
    dict[s2] = strperdiv2
    # print dict

    cursor.execute("select count(*) from jdproducts where reallyPrice >= %s and reallyPrice <=%s" % (div2, max))
    # print sql
    div3num = cursor.fetchone()
    div3num = div3num[0]
    # print div3num
    perdiv3 = 100 - perdiv2 - perdiv1

    s3 = '' + str(div2) + '--' + str(max)
    strperdiv3 = str(perdiv3)
    dict[s3] = strperdiv3
    print dict

    return JsonResponse(dict)

def show_productdetail(request,productid):
    infos = models.Jdproduct.objects.filter(url=productid)[:1]
    return render(request, 'spider/show_productdetail.html',{'infos': infos}) #json.dumps(info)})

def getdifferentprice(request,productid):
    cursor = connection.cursor()
    cursor.execute("select * from jdproduct where url = '%s' "%(productid))
    result = cursor.fetchall()

    if result !=None:
        product_name = re.search(u'【(.*?)】',result[0][1]).group(1)
    # print product_name

    pricelist = []
    for eachresult in result:
        dict={eachresult[13]:eachresult[4]}
        pricelist.append(dict)
    result={product_name:pricelist}
    return JsonResponse(result)

#停止
def stop(request):
    if request.method == 'POST':
        jobid = request.POST['jobid']
        type = request.POST['type']

    if type == 'jd':
        jdspider.cancel(jobid)
    if type == 'tb':
        tbspider.cancel(jobid)
    if type == 'wy':
        wyspider.cancel(jobid)
    dict = {'result':'停止成功'}
    return JsonResponse(dict)

#删除
def delete(request):
    if request.method == 'POST':
        jobid = request.POST['jobid']

    task = models.Task.objects.get(jobid = jobid)
    task.delete()
    dict = {'result':'删除成功'}
    return JsonResponse(dict)


