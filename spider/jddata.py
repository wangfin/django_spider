# -*- coding: utf-8 -*-
from handledb import MysqldbHelper
import MySQLdb
import decimal
import re


# 获取价格最高和最低的五个商品
# 返回两个列表
def getprice():
    

    #cursor = connection.cursor()

    # Data modifying operation
    #cursor.execute("select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) limit 0,5")
    #transaction.set_dirty()
    #cursor.execute("alter table jdproducts auto_increment=1")
    #transaction.set_dirty()

    row = cursor.fetchone()
    sqlhepler = MysqldbHelper()
    conn = sqlhepler.getCon()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) limit 0,5'
    count = cur.execute(sql)
    result = cur.fetchall()

    # 价格最低的前五个商品
    for eachresult in result:
        print eachresult['reallyPrice']

    # 价格排行最高的五个商品
    sql = 'select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) DESC limit 0,5'
    count = cur.execute(sql)
    result2 = cur.fetchall()
    for eachresult in result2:
        print eachresult['reallyPrice']
    # print result


    return result,result2



# {'4000.0--5688.0': '7.0%', '2400.0--4000.0': '32.0%', '799.0--2400.0': '61.0%'}
# 构造价格区间所在比例
def getpricediv():
    sqlhepler = MysqldbHelper()
    conn = sqlhepler.getCon()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) limit 0,1'
    count = cur.execute(sql)
    result = cur.fetchall()
    min = result[0]['reallyPrice']
    # print min

    sql = 'select count(*) from jdproducts'
    count = cur.execute(sql)
    num = cur.fetchone()
    num = num['count(*)']
    # print num

    sql = 'select * from jdproducts ORDER BY cast(reallyPrice as DECIMAL(32,2)) DESC limit 0,1'
    count = cur.execute(sql)
    result2 = cur.fetchall()
    max = result2[0]['reallyPrice']
    # print max

    cha = max - min
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

    sql = "select count(*) from jdproducts where reallyPrice >= %s and reallyPrice <=%s"%(min,div1)
    # print sql
    count = cur.execute(sql)
    div1num = cur.fetchone()
    div1num = div1num['count(*)']
    # print div1num
    perdiv1 = round(div1num*100/num,3)
    # print perdiv1

    s = ''+str(min) + '--'+str(div1)
    strperdiv1 = str(perdiv1)+'%'
    dict = {s:strperdiv1}
    # print dict

    sql = "select count(*) from jdproducts where reallyPrice >= %s and reallyPrice <=%s" % (div1, div2)
    # print sql
    count = cur.execute(sql)
    div2num = cur.fetchone()
    div2num = div2num['count(*)']
    # print div2num
    perdiv2 = round(div2num * 100 / num, 3)

    s2 = '' + str(div1) + '--' + str(div2)
    strperdiv2 = str(perdiv2) + '%'
    dict[s2] = strperdiv2
    # print dict


    sql = "select count(*) from jdproducts where reallyPrice >= %s and reallyPrice <=%s" % (div2, max)
    # print sql
    count = cur.execute(sql)
    div3num = cur.fetchone()
    div3num = div3num['count(*)']
    # print div3num
    perdiv3 = 100 - perdiv2 - perdiv1

    s3 = '' + str(div2) + '--' + str(max)
    strperdiv3 = str(perdiv3) + '%'
    dict[s3] = strperdiv3
    print dict

    return dict

# 获取好评数以及好频率和原价差价最大的几个商品,差评率
def getcomment():
    sqlhepler = MysqldbHelper()
    conn = sqlhepler.getCon()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = 'select * from jdproducts'
    count = cur.execute(sql)
    result = cur.fetchall()


    max = 0
    maxper = 0
    maxpooroer = 0
    maxchajia = 0

    for eachresult in result:
        # eachdata = eachresult['AllCount']
        if u'万' in eachresult['AllCount']:
            eachdata = float(eachresult['AllCount'].replace(u'万',''))*10000
            # print eachdata
        else:
            eachdata = float(eachresult['AllCount'])
        if int(eachdata)>max:
            max = eachdata
            maxid = eachresult['_id']
            maxurl = eachresult['url']
            maxname = re.search(u'【(.*?)】',eachresult['names']).group(1)


        if u'万' in eachresult['GoodCount']:
            eachgooddata = float(eachresult['GoodCount'].replace(u'万',''))*10000
            # print eachdata
        else:
            eachgooddata = float(eachresult['GoodCount'])
        eachper = round(eachgooddata * 100 / eachdata,3)
        if(eachper>maxper):
            maxper = eachper
            maxpernames = re.search(u'【(.*?)】',eachresult['names']).group(1)
            maxperurl = eachresult['url']

        if u'万' in eachresult['PoorCount']:
            eachpoordata = float(eachresult['PoorCount'].replace(u'万',''))*10000
            print eachdata
        else:
            eachpoordata = float(eachresult['PoorCount'])
        eachpoorper = round(eachpoordata * 100 / eachdata,3)
        if(eachpoorper>maxpooroer):
            maxpooroer = eachpoorper
            maxpoornames = re.search(u'【(.*?)】',eachresult['names']).group(1)
            maxpoorurl = eachresult['url']

        eachchajia = float(eachresult['originalPrice']) - float(eachresult['reallyPrice'])
        if eachchajia>maxchajia:
            maxchajia = eachchajia
            maxchajianames = re.search(u'【(.*?)】',eachresult['names']).group(1)
            maxchajiaurl = eachresult['url']

    # 存储的时评论数最多的评论数和商品名字以及商品链接
    dict1 ={"max":max}
    dict1['maxname'] = maxname
    dict1['maxurl'] = maxurl

    print dict1
    # 存储好频率最多好评率以及商品的名字和商品链接
    dict2 = {"maxper":maxper}
    dict2['maxpernames'] = maxpernames
    dict2['maxperurl'] = maxperurl
    print dict2

    #存储差评率最高的差评率以及商品的名字和商品链接
    dict3 = {"maxpoorper":maxpooroer}
    dict3['maxpoornames'] = maxpoornames
    dict3['maxpoorurl'] = maxpoorurl
    print dict3

    # 存储和原来价格差价最高的差价以及商品名字和商品链接
    dict4 = {'maxchajia':maxchajia}
    dict4['maxchajianames'] = maxchajianames
    dict4['maxchajiaurl'] = maxchajiaurl
    print dict4

    return dict1,dict2,dict3,dict4

    # print 'the max is', max
    # print 'the maxid is', maxid
    # print 'the maxname is ', maxname
    #
    # print u'好评率最高的商品是',maxper
    # print u'name is',maxpernames
    # print maxpooroer
    # print '差频率最高的商品',maxpoornames
    # print '差价最高的商品',maxchajianames,maxchajia








if __name__ == '__main__':
    # getpricediv()
    # results = getprice()
    #
    #
    # print results[0][0]['AfterCount']

    # getcomment()
    getpricediv()

    # s = '1.3'
    # print decimal.Decimal(s)*10000
