import sys
from handledb import MysqldbHelper

import socket
import urllib2


def counter(start_at = 0):
    '''Function: count number
    Usage: f = d=fuction(i) print f() #i+1
    '''
    count = [start_at]
    def incr():
        count[0] + 1
        return count[0]
    return incr

def use_proxy(browser,proxy,url):
    '''open broswer with proxy'''
    #After visited transfer ip
    profile = browser.profile
    profile.set_preference('network.proxy.type',1)
    profile.set_preference('network.proxy.http',proxy[0])
    profile.set_preference('network.proxy.http_port',int(proxy[1]))
    profile.set_preference('permissions.default.image',2)
    profile.update_preference()
    browser.profile = profile
    browser.get(url)
    browser.implicitly_wait(30)
    return browser


class Singleton(object):
    '''Signal instance example'''

    def __new__(cls, *args, **kw):
        if not hasattr(cls,'_instance'):
            orig = super(Singleton,cls)
            cls.__instance = orig.__new__(cls,*args,**kw)
        return cls.__instance

class GetIp(Singleton):
    sqlHelper = MysqldbHelper()
    def __init__(self):
        sql = '''SELECT IP,PORT,TYPE
                 FROM proxy
                 WHERE 
                 'SPEED'<5 OR 'SPEED' IS NULL 
                 ORDER BY 'TYPE' ASC 
                 LIMIT 20
         '''
        self.result = MysqldbHelper().select(sql)
        print 'result is',self.result

    def del_ip(self,record):
        '''delete ip that can not use'''
        sql = "delete from proxy where IP='%s' and PORT = '%s'"%(record['IP'],record['PORT'])
        print sql
        MysqldbHelper().select(sql)
        MysqldbHelper().getCon().commit()
        print record,"was deleted"

    def judge_ip(self,record):
        '''Judge IP can use or not'''
        http_url = 'http://www.baidu.com/'
        https_url = "https://www.alipay.com/"
        # print record
        proxy_type = record['TYPE'].lower()
        url = http_url if proxy_type == 'http' else https_url
        proxy = "%s:%s"%(record['IP'],record['PORT'])
        try:
            req = urllib2.Request(url = url)
            req.set_proxy(proxy,proxy_type)
            response = urllib2.urlopen(req)
        except Exception,e:
            print "Request Error:",e
            self.del_ip(record)
            return False
        else:
            code = response.getcode()
            if code>=200 and code<300:
                print 'Effctive proxy',record
                return True
            else:
                print 'Invalid proxy',record
                self.del_ip(record)
                return False

    def get_ips(self):
        print "Proxy getip was executed"
        http =[]
        https = []
        for h in self.result:
            print h
            if h["TYPE"] == "HTTP":
                # if self.judge_ip(h):
                http.append(h)
            elif h["TYPE"] == "HTTPS":
            # https = [h for h in self.result if h[3] == "HTTPS" and self.judge_ip(h)]
            #     if self.judge_ip(h):
                https.append(h)
        print '--------------------'
        for eachhttp in http:
            print eachhttp
        print '------------------------'
        for eachhttps in https:
            print eachhttps
        print "HTTP:",len(http),"HTTPS:",len(https)
        return {"http":http,"https":https}

