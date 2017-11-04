# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

import redis

from timing import Timing
from . models import TimingTask
from . import models
time_task = Timing()

# 计算优先级

class TimingPriority():
    def calculate(self,name,type, priority, setime,timing_number,timing_type,url,start_minutes,end_minutes):
        # 计算优先级
        level = 0
        # 为电商类网站
        if type == "jd_products" or type == "tb_products":
            level += 2
        else:
            level += 0
        # 计算本身的优先级
        level = level + int(priority)

        #计算时间
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz)
        now_time = now.strftime("%m/%d/%Y")
        start_time = setime.split(' - ', 1)[0]
        end_time = setime.split(' - ', 1)[1]

        level += 2
        #level = level/int(depth) + 1
        if type == 'jd_products':
            print "开始运行jd单个商品"
            obj = models.TimingTask(name=name,url=url,starttime=now_time,runnumber=0)
            obj.save()
            time_task.start(name,type,timing_type,timing_number,start_time,end_time,start_minutes,end_minutes)
            
        elif type == 'tb_products': 
            print "开始运行tb单个商品"
            obj = models.TimingTask(name=name,url=url,starttime=now_time,runnumber=0)
            obj.save()
            time_task.start(name,type,timing_type,timing_number,start_time,end_time,start_minutes,end_minutes)       
          

        return level
