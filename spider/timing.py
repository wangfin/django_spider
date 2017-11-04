# coding=utf-8
import os
import redis
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from apscheduler.schedulers.background import BackgroundScheduler
import logging
from JdSingleSpider import JdSingleSpider
from TbSingleSpider import TbSingleSpider
        
class Timing():
    def start(self,name,type,timing_type,timing_number,start_time,end_time,start_minutes,end_minutes):
        #jobstores = {
            #'redis': RedisJobStore(),
          #}
        #executors = {
            #'default': ThreadPoolExecutor(10),
            #'processpool': ProcessPoolExecutor(3)
          #}
        logging.basicConfig()
        scheduler = BackgroundScheduler(timezone='Asia/Shanghai')#jobstores=jobstores, executors=executors, 
        number = int(timing_number)
        start_time_en = start_time.encode("utf-8")
        end_time_en = end_time.encode("utf-8")
        start_minutes_en = start_minutes.encode("utf-8")
        end_minutes_en = end_minutes.encode("utf-8")
        start = start_time_en.split('/')[2]+"-"+start_time_en.split('/')[0]+"-"+start_time_en.split('/')[1]+" "+start_minutes_en
        end = end_time_en.split('/')[2]+"-"+end_time_en.split('/')[0]+"-"+end_time_en.split('/')[1]+" "+end_minutes_en
        #print end,timing_type
        jdsinglespider = JdSingleSpider() 
        tbsinglespider = TbSingleSpider() 
        if type == "jd_products":
            if timing_type == "second":
                job = scheduler.add_job(jdsinglespider.run, 'interval', seconds = number,start_date=start, end_date=end,args=[name])#,jobstore='redis'
            elif timing_type == "minute":
                job = scheduler.add_job(jdsinglespider.run, 'interval', minutes = number,start_date=start,end_date=end,args=[name])
            elif timing_type == "hour":
                job = scheduler.add_job(jdsinglespider.run, 'interval', hours = number,start_date=start,end_date=end,args=[name])
            elif timing_type == "day":
                job = scheduler.add_job(jdsinglespider.run, 'interval', days = number,start_date=start,end_date=end,args=[name])
            elif timing_type == "week":
                job = scheduler.add_job(jdsinglespider.run, 'interval', weeks = number,start_date=start,end_date=end,args=[name])

            try:
                scheduler.start()    #采用的是非阻塞的方式
            except (KeyboardInterrupt, SystemExit):
                # Not strictly necessary if daemonic mode is enabled but should be done if possible
                scheduler.shutdown()
                print('Exit The Job!')
        elif type == "tb_products":
            if timing_type == "second":
                job = scheduler.add_job(tbsinglespider.run, 'interval', seconds = number,start_date=start, end_date=end,args=[name])
            elif timing_type == "minute":
                job = scheduler.add_job(tbsinglespider.run, 'interval', minutes = number,start_date=start, end_date=end,args=[name])
            elif timing_type == "hour":
                job = scheduler.add_job(tbsinglespider.run, 'interval', hours = number,start_date=start, end_date=end,args=[name])
            elif timing_type == "day":
                job = scheduler.add_job(tbsinglespider.run, 'interval', days = number,start_date=start, end_date=end,args=[name])
            elif timing_type == "week":
                job = scheduler.add_job(tbsinglespider.run, 'interval', weeks = number,start_date=start, end_date=end,args=[name])
                
    
            #print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
            #print type,timing_type,timing_number
            #print self.job

            try:
                scheduler.start()    #采用的是非阻塞的方式
            except (KeyboardInterrupt, SystemExit):
                # Not strictly necessary if daemonic mode is enabled but should be done if possible
                scheduler.shutdown()
                print('Exit The Job!')
            

    def pause(self):
        job.pause()
        print "暂停"
    
    def delete(self):
        job.remove()
        print "移除任务"


