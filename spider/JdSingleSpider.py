# coding=utf-8
import urllib
import urllib2
import time
from .models import TimingTask
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 

class JdSingleSpider():
    def start(self,name):
        # 启动爬虫
        test_data = {'project':'Jdsingle', 'spider':'JdSingleSpider','url':name}
        test_data_urlencode = urllib.urlencode(test_data)

        requrl_master = "http://192.168.159.146:6800/schedule.json"

        # 以下是post请求
        req = urllib2.Request(url = requrl_master, data = test_data_urlencode)
        #print test_data_urlencode
		  
        res_data = urllib2.urlopen(req)
        #print res_data.jobid
        res_master = res_data.read()  # res 是str类型
        print res_master
        result_master = eval(res_master)
        return result_master['jobid']

    def run(self,name):
        # 启动爬虫
        task = TimingTask.objects.get(name=name)  # 查询该条记录，任务名称不能重复
        number = task.runnumber
        num = int(number) + 1
        task.runnumber = num  # 修改运行次数
        task.save()
        test_data = {'project':'Jdsingle', 'spider':'JdSingleSpider','url':name}
        test_data_urlencode = urllib.urlencode(test_data)

        requrl_master = "http://192.168.159.146:6800/schedule.json"

        # 以下是post请求
        req = urllib2.Request(url = requrl_master, data = test_data_urlencode)
		  
        res_data = urllib2.urlopen(req)
        print "运行爬虫"
          
             
        
