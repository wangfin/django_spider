# -*- coding: utf-8 -*-
import time
from .models import TimingTask
import pytz
from datetime import datetime

class Timing_check():
    def check(self,name):
        task = TimingTask.objects.get(name=name)
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz)
        now_time = now.strftime("%m/%d/%Y %H:%M:%S")
        now_time_mk = time.mktime(time.strptime(now_time, "%m/%d/%Y %H:%M:%S"))#now.timestamp() #time.mktime(time.strptime(now_time, "%m/%d/%Y %H:%M:%S"))
        #print now,now_time_mk
            #用户输入的时间
        start_time = task.time.split(' - ', 1)[0]+" "+task.start_minutes
        end_time = task.time.split(' - ', 1)[1]+" "+task.end_minutes
        #print start_time,end_time

         #转换成时间戳
        start_time_mk = time.mktime(time.strptime(start_time, "%m/%d/%Y %H:%M:%S"))
        end_time_mk = time.mktime(time.strptime(end_time, "%m/%d/%Y %H:%M:%S"))
        #print start_time_mk,end_time_mk

        if now_time_mk < start_time_mk:#等待
           task.runtype = "denying"
        elif now_time_mk > end_time_mk:#结束
           task.runtype = "finished"
        elif now_time_mk > start_time_mk and now_time_mk < end_time_mk: #运行中
           task.runtype = "running"

        task.save()
