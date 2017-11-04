# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import MySQLdb
from handledb import MysqldbHelper

class getPara:

    def getpara(self):
        start = raw_input("输入url")
        wantnum = raw_input("请输入爬取的条数")
        direct = raw_input("1表示向上2表示向下爬取")
        
        

        dict = {'url': start,
                'direct':direct,
                'wantnum':wantnum
               }
        return dict



# url = ''
# res = get_totalpage(url)
# print res[0],res[1],res[2],res[3],res[4]
