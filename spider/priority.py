# -*- coding: utf-8 -*-
import time
import pytz
from datetime import datetime

import redis


from JDspider import JDspider
from TBspider import TBspider
from WYspider import WYspider
from CSDNspider import CSDNspider
from . models import Task
from . import models
jdspider = JDspider()
tbspider = TBspider()
wyspider = WYspider()
csdnspider = CSDNspider()
# 该类是为了获取爬取深度的页数
# 创建redis连接池
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)
# 计算优先级

class Priority():
    def calculate(self,name,type, priority, setime, depth):
        # 计算优先级
        level = 0
        # 为电商类网站
        if type == "jd" or type == "tb":
            level += 2
        else:
            level += 0
        # 计算本身的优先级
        level = level + int(priority)

        #计算时间
        #now_time = time.strftime("%m/%d/%Y", time.localtime())
        #now_time_mk = time.mktime(time.strptime(now_time, "%m/%d/%Y"))
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz)
        now_time = now.strftime("%m/%d/%Y")
        now_time_mk = time.mktime(time.strptime(now_time, "%m/%d/%Y"))
        print now_time_mk

        #用户输入的时间
        start_time = setime.split(' - ', 1)[0]
        end_time = setime.split(' - ', 1)[1]

        start_year = int(start_time.split('/')[2])
        start_month = int(start_time.split('/')[0])-1
        start_day = int(start_time.split('/')[1])

        end_year = int(end_time.split('/')[2])
        end_month = int(end_time.split('/')[0])-1
        end_day = int(end_time.split('/')[1])

        #转换成时间戳
        start_time_mk = time.mktime(time.strptime(start_time, "%m/%d/%Y"))
        end_time_mk = time.mktime(time.strptime(end_time, "%m/%d/%Y"))
        print start_time_mk

        #run_time_mk = end_time_mk - start_time_mk #可以进行运行的时间

        if (now_time_mk == start_time_mk):
            level += 2
            level = level/int(depth) + 1
            if type=='jd':
                print "开始运行京东"
                #存入运行时间为现在 now_time 为 starttime
                #存入运行状态为开始
                # 存入mysql数据库
                obj = models.Task(name=name,starttime=now_time,runtype="running",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                task = Task.objects.get(name=name)  # 查询该条记录
                r.set('jd_taskid', task.id)
                jobid = jdspider.start()
                task.jobid = jobid  # 修改
                task.save()  # 保存
                jdspider.check(jobid)
            elif type=='tb':
                print "开始运行淘宝"
                obj = models.Task(name=name, starttime=now_time, runtype="running",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                task = Task.objects.get(name=name)  # 查询该条记录
                r.set('tb_taskid', task.id)
                jobid = tbspider.start()
                task.jobid = jobid  # 修改
                task.save()  # 保存
                #JDspider.start()
                tbspider.check(jobid)
            elif type=='wy':
                print "开始运行网易"
                obj = models.Task(name=name, starttime=now_time, runtype="running",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                task = Task.objects.get(name=name)  # 查询该条记录
                r.set('wy_taskid', task.id)
                jobid = wyspider.start()
                task.jobid = jobid
                task.save()  # 保存
                wyspider.check(jobid)
            elif type=='csdn':
                print "开始运行csdn"
                obj = models.Task(name=name, starttime=now_time, runtype="running",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                task = Task.objects.get(name=name)  # 查询该条记录
                r.set('csdn_taskid', task.id)
                jobid = csdnspider.start()
                task.jobid = jobid
                task.save()  # 保存
                csdnspider.check(jobid)
        #elif (start_time_mk > now_time_mk):
            #run_time = run_time_mk / 3600 / 24
            #level = level / run_time

            #obj = models.Task(name=name,starttime="未开始", runtype="pending")
            #obj.save()

        else:#这里是当用户需要运行的时间与当前时间不一致时，设置定时任务，到时间触发
            level += 0
            level = level/int(depth) + 1
            if type=='jd':
                print "等待运行京东"
                #存入运行时间为现在 now_time 为 start_time用户输入开始时间
                #存入运行状态为等待
                # 存入mysql数据库
                obj = models.Task(name=name,starttime=start_time,runtype="denying",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                #task = Task.objects.get(name=name)  # 查询该条记录
                #r.set('jd_taskid', task.id)
                #jobid = jdspider.start()
                #task.jobid = jobid  # 修改
                #task.save()  # 保存
                #jdspider.check(jobid)
            elif type=='tb':
                print "等待运行淘宝"
                obj = models.Task(name=name, starttime=start_time, runtype="denying",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                #task = Task.objects.get(name=name)  # 查询该条记录
                #r.set('tb_taskid', task.id)
                #jobid = tbspider.start()
                #task.jobid = jobid  # 修改
                #task.save()  # 保存
                #JDspider.start()
                #tbspider.check(jobid)
            elif type=='wy':
                print "等待运行网易"
                obj = models.Task(name=name, starttime=start_time, runtype="denying",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                #task = Task.objects.get(name=name)  # 查询该条记录
                #r.set('wy_taskid', task.id)
                #jobid = wyspider.start()
                #task.jobid = jobid
                #task.save()  # 保存
                #wyspider.check(jobid)
            elif type=='csdn':
                print "等待运行csdn"
                obj = models.Task(name=name, starttime=start_time, runtype="denying",start_year=start_year,start_month=start_month,start_day=start_day,end_year=end_year,end_month=end_month,end_day=end_day)
                obj.save()
                #task = Task.objects.get(name=name)  # 查询该条记录
                #r.set('csdn_taskid', task.id)
                #jobid = csdnspider.start()
                #task.jobid =
                #task.save()  # 保存
                #csdnspider.check(jobid)

        return level
