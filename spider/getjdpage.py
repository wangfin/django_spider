# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re
import MySQLdb
from handledb import MysqldbHelper

class getJDPage():


    def getUrlBySearchname(self,keyname):
        # print u'keyname is',keyname

        conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
        cur = conn.cursor(MySQLdb.cursors.DictCursor)

        sqlHelper = MysqldbHelper()
        # keyname = '%'+keyname+'%'
        print keyname
        sql = "select * from jdmenu where names = '%s'" % keyname
        # print sql
        result = sqlHelper.select(sql)
        print result
        pass

        if result.__len__() == 0:
            result = ({'url': 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % keyname, 'names': keyname},)
            # result[0]['name'] = keyname
            # result[0]['url'] = 'https://search.jd.com/Search?keyword=%s&enc=utf-8'%keyname

        return result



    def get_totalpage(self,url):



        if re.findall(r'/', url).__len__() != 0:
            html = requests.get(url)
            selector = etree.HTML(html.content)
            isurl = '1'
            try:
                flag = '2'
                totalpage = selector.xpath('//div[@id="J_topPage"]/span/i/text()')[0]
                totalcount = selector.xpath('//div[@class="f-result-sum"]/span/text()')[0]
            except:
                totalpage = None
                totalcount = None
                flag = '1'

            # 返回字典型
            dict = {'totalpage':totalpage,
                    'totalcount':totalcount,
                    'flag':flag,
                    'isurl':isurl,
                    'url':url}
            return dict

        else:
            isurl = '2'
            flag = '0'
            resurl = self.getUrlBySearchname(url)
            print resurl[0]['names'], resurl[0]['url']
            html = requests.get(resurl[0]['url'])

            selector = etree.HTML(html.content)

            try:
                totalpage = selector.xpath('//span[@class="p-skip"]/em/b/text()')[0]
                totalcount = selector.xpath('//div[@class="st-ext"]/span/text()')[0]
                # print u'这类商品共有', pageall, u'页'
            except Exception as e:
                print u'该url没有总页数'
                totalpage = 100
                totalcount = None
            dict = {'totalpage': totalpage,
                    'totalcount': totalcount,
                    'flag': flag,
                    'isurl': isurl,
                    'url': resurl[0]['url']}
            return dict



# url = ''
# res = get_totalpage(url)
# print res[0],res[1],res[2],res[3],res[4]
