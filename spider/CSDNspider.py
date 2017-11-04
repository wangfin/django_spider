# coding=utf-8
import urllib
import urllib2
import time
from . import models
from .models import Task


class CSDNspider():
    def start(self):
        # 启动爬虫
        test_data = {'project': 'csdn', 'spider': 'CSDNBlogCrawlSpider'}
        test_data_urlencode = urllib.urlencode(test_data)

        requrl_master = "http://192.168.159.146:6800/schedule.json"
        requrl_server = "http://192.168.159.147:6800/schedule.json"

        # 以下是post请求
        req = urllib2.Request(url=requrl_master, data=test_data_urlencode)
        req1 = urllib2.Request(url=requrl_server, data=test_data_urlencode)

        res_data = urllib2.urlopen(req)
        res_data1 = urllib2.urlopen(req1)
        # print res_data.jobid
        res_master = res_data.read()  # res 是str类型
        res_server = res_data1.read()
        # print res
        result_master = eval(res_master)
        result_server = eval(res_server)
        return result_master['jobid'] + "," + result_server['jobid']

    def cancel(self, jobid):
        # 首先拆分jobid，这个jobid是主机与从机一起拼接在一起的字符串，用逗号隔开
        jobid_master = jobid.split(',', 1)[0]
        jobid_server = jobid.split(',', 1)[1]
        # 停止爬虫
        test_data = {'project': 'csdn', 'job': jobid_master}
        test_data_urlencode = urllib.urlencode(test_data)

        test_data1 = {'project': 'csdn', 'job': jobid_server}
        test_data_urlencode1 = urllib.urlencode(test_data1)

        # requrl = "http://192.168.159.142:6800/cancel.json"
        requrl_master = "http://192.168.159.146:6800/cancel.json"
        requrl_server = "http://192.168.159.147:6800/cancel.json"

        # 以下是post请求 主机和从机全部停止
        req = urllib2.Request(url=requrl_master, data=test_data_urlencode)
        req1 = urllib2.Request(url=requrl_server, data=test_data_urlencode1)

        res_data = urllib2.urlopen(req)
        res_data1 = urllib2.urlopen(req1)
        res = res_data.read()  # res 是str类型
        print res
        # result = eval(res)
        # if result['status'] == "ok":
        # task = models.Task.objects.get(jobid=jobid)
        # task.runtype = "finished"
        # task.save()

    def check(self, jobid):
        jobid_master = jobid.split(',', 1)[0]
        jobid_server = jobid.split(',', 1)[1]
          # 查询爬虫
        myproject = "csdn"
        requrl = "http://192.168.159.146:6800/listjobs.json?project=" + myproject#主机
        requrl1 = "http://192.168.159.147:6800/listjobs.json?project=" + myproject#从机
        req = urllib2.Request(requrl)
        req1 = urllib2.Request(requrl1)

        res_data = urllib2.urlopen(req)
        res_data1 = urllib2.urlopen(req1)

        res = res_data.read()
        result = eval(res)
 
        res1 = res_data1.read()
        result1 = eval(res1) 
        #print result['finished'][1]
        task = models.Task.objects.get(jobid=jobid)
        if result['pending'] != []:
            for i in range(len(result['pending'])):
                type = result['pending'][i]
                if jobid_master == type['id']:
                    task.runtype = "pending"
                    task.save()
        if result['running'] != [] or result1['running'] != []:
            run_time_mk = 0;run_time_mk1 = 0;
            for i in range(len(result['running'])):
                type = result['running'][i]
                if jobid_master == type['id']:
                    task.runtype = "running"
                    start_time_mk = time.mktime(time.strptime(type['start_time'], "%Y-%m-%d %H:%M:%S.%f"))
                    end_time_mk = time.time()#当前时间
                    run_time_mk = end_time_mk - start_time_mk
            for i in range(len(result1['running'])):
                type1 = result1['running'][i]
                if jobid_server == type1['id']:
                    task.runtype = "running"
                    start_time_mk1 = time.mktime(time.strptime(type1['start_time'], "%Y-%m-%d %H:%M:%S.%f"))
                    end_time_mk1 = time.time()#当前时间
                    run_time_mk1 = end_time_mk1 - start_time_mk1

            if run_time_mk != 0 and run_time_mk1 != 0:
                mk = max(run_time_mk, run_time_mk1)
                #mk = run_time_mk
                st = time.localtime(mk)  # 运行时间戳
                run_time = time.strftime('%M:%S', st)  # 运行时间
                task.runtime = run_time
                task.save()

        if result['finished'] != [] and result1['finished'] != []:
            run_time_mk = 0;run_time_mk1 = 0;
            for i in range(len(result['finished'])):
                type = result['finished'][i]
                if jobid_master == type['id']:
                    start_time_mk = time.mktime(time.strptime(type['start_time'], "%Y-%m-%d %H:%M:%S.%f"))
                    end_time_mk = time.mktime(time.strptime(type['end_time'], "%Y-%m-%d %H:%M:%S.%f"))
                    run_time_mk = end_time_mk - start_time_mk
                    
            for i in range(len(result1['finished'])):
                type1 = result1['finished'][i]
                if jobid_server == type1['id']:
                    start_time_mk1 = time.mktime(time.strptime(type1['start_time'], "%Y-%m-%d %H:%M:%S.%f"))
                    end_time_mk1 = time.mktime(time.strptime(type1['end_time'], "%Y-%m-%d %H:%M:%S.%f"))
                    run_time_mk1 = end_time_mk1 - start_time_mk1
            
            if run_time_mk != 0 and run_time_mk1 != 0:
                task.runtype = "finished"
                mk = max(run_time_mk, run_time_mk1)
                #mk = run_time_mk
                st = time.localtime(mk)#运行时间戳
                run_time = time.strftime('%M:%S', st)#运行时间
                task.runtime = run_time
                task.save()  
        
