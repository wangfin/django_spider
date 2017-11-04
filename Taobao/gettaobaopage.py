# -*- coding: utf-8 -*-
import requests
from lxml import etree
import re

class TaoBaoPage():

    def start(self,url):
        pageres = ''
        isdataSource = '0'
        isapiData = '0'
        resurl = ''
        resurl2 = ''
        dataurl = ''
        if re.findall(r'taobao', url).__len__() != 0:
            isTaobao = '1'
            html = requests.get(url)
            selector = etree.HTML(html.content)
            if re.findall(r'g_page_config', html.content).__len__() != 0:
                isdataSource = '1'
                print u'该页面数据来源于页面源代码'
                pageres = self.getPageinfo(url)
            else:
                isdataSource = '2'
                print u'该页面的数据来源于ajax'
                # 从页面源代码获取数据页面的参数
                if selector.xpath('//input[@id="J_FirstAPI"]/@value').__len__() != 0:
                    isapiData = '1'
                    paras = selector.xpath('//input[@id="J_FirstAPI"]/@value')[0]
                    print 'paras is', paras
                    dataurl = "https://list.taobao.com/itemlist/acg.htm?_input_charset=utf-8&json=on&%s" % paras
                    print dataurl
                    #此处有request解析
                    # self.getajaxdata(dataurl)
                else:
                    isapiData = '2'
                    tce_sid = self.gettce_sid(url)
                    newurl = 'https://tce.taobao.com/api/mget.htm?tce_sid=%s' % tce_sid[0]
                    print newurl
                    #此处有request解析
                    resurl=newurl
                    resurl2 = 'https://www.taobao.com/go/rgn/sys/xctrl/dispatch.php?murl=http://tce.taobao.com/api/get.htm&tce_sid=%s' % tce_sid[1][0]
                    for i in range(1,tce_sid[1].__len__()):
                        newurl2 = 'https://www.taobao.com/go/rgn/sys/xctrl/dispatch.php?murl=http://tce.taobao.com/api/get.htm&tce_sid=%s' % tce_sid[1][i]
                        resurl2 = '%s,%s'%(resurl2,newurl2)
                        #request解析

        else:
            isTaobao = '2'
            cookies4 = {
                'cookie': '_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=249201; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZeeFqgcQ%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51Rq6%2FNrmhSY8%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; tt=sec.taobao.com; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=117UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAfUVxTHRAdSM%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhSbVdqUmZbY1diVWhKckdySH1EcE15RXhNdk5wSmQy%7CVWldfS0SMg04DS0RLg4gVWhUalVrTmdcYkdiTBpM%7CVmhIGCwWNgsrESoUNA4xDzQUKBYtFjYMNwIiHiAbIAA6BTBmMA%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A990*7236-client%3A763*588-offset%3A763*7236-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=Ao2N2IE56FIyCk061dJQpE9pnKnHwkI95gKrr88SySSTxq14l7rRDNtcREd1',
                'cookie': '_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=249201; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZeeFqgcQ%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51Rq6%2FNrmhSY8%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; tt=sec.taobao.com; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=111UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAekN8R3pFfCo%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhSbVdtVGtQbVJrXGFDf0p%2BR3pAeEB4Q39LdEx1T2E3%7CVWldfS0QMAsxDy8TJgYoVHMAcwk%2FSypEYBAsSToKOh4jDVsN%7CVmhIGCwWNgsrFykQJAQ%2FAjwBIR0jGCMDOQI3FysVLhU1DzAFUwU%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1349*6030-client%3A1349*605-offset%3A1349*6030-screen%3A1366*768; isg=Ajg4V0rklaUNBvhlyIldE5piCeYKCR8qU5n-EHKphHMmjdh3GrFsu06vMZjo',
                'cookie': '_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=249201; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZeeFqgcQ%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51Rq6%2FNrmhSY8%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=075UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAekN9QX9KcSc%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhSbVdtVGpWaF1mUWxOcUlzT3JLckxwSHRIfUN6RX5QBg%3D%3D%7CVWldfS0SMg4wDS0VNRswEC8PMB5IHg%3D%3D%7CVmhIGCwWNgsrESoUNA4xDDcXKxUuFTUPNAEhHSMYIwM5BjNlMw%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A990*7206-client%3A763*588-offset%3A763*7206-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=Ai0t-BmNCLL_K-0aNfKwhO-JPMlnIuJdRiJLj28yA0Qz5k2YN9pxLHv0pKfV',
                'cookie': '_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=ArCw4tCemYbgtfSHX3n13WUuAHABEpRK; _tb_token_=7c7c103738e7; uc1=cookie14=UoW%2Bv%2FZf7Aod8g%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=Vq8l%2BKCLjhS4UhJVbCU7&tag=8&cookie15=URm48syIIVrSKA%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51RzG9N6wxayE%3D&lg2=URm48syIIVrSKA%3D%3D; uss=U7PCzlBnZyD0Ajm09IOMPBOwnivCPLuM7eQpVmberdPQ%2BqZYAIL1Ytt3TA%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=10b75e1acc8da7caaee0058b116d26ef; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=e8823214ea1fe4e93a65b5419a02f29b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; tt=login.tmall.com; cna=VGrXDroWdwACAXAZiUThcFIk; pnm_cku822=166UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAdUhxTnNOcyU%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhSbVdiX2ZZZFlkU25MeEdyR39LdEt3QnhEeU12TmA2%7CVWldfS0SMg04DCwQJAQqFysVKhQxGCMdOB1vEkIpf09kM2RKHEo%3D%7CVmhIGCUFOBgkGiMXNwwxCjcXKxUuFTUPNAEhHSMYIwM5BjNlMw%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1349*6060-client%3A1349*662-offset%3A1349*6060-screen%3A1366*768; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=23207; whl=-1%260%260%260; isg=AszMm7mH-SGExuwbaQZG4Q8znSo-rVvy2r--zSaN23casWy7ThVAP8IDJY9y'
            }
            html = requests.get(url, cookies=cookies4)
            # print html.content
            selector = etree.HTML(html.content)
            pageall = selector.xpath('//input[@name="totalPage"]/@value')[0]
            pagenow = selector.xpath('//input[@name="jumpto"]/@value')[0]
            pagecount = selector.xpath('//p[@class="crumbTitle j_ResultsNumber"]/span/text()')[0]
            # pageres.append(pageall)
            # pageres.append(pagenow)
            # pageres.append(pagecount)
            pageres = '%s,%s,%s'%(pageall,pagenow,pagecount)
            print u'该类商品共有', pageall, u'页', u'当前页是', pagenow, u'页'

            dict = {'isTaobao': isTaobao,
                    'isdataSource': isdataSource,
                    'isapiData': isapiData,
                    'pageres': pageres,
                    'resurl': resurl,
                    'resurl2':resurl2,
                    'url':url,
                    'dataurl':dataurl
                    }

        return dict




    def getPageinfo(url):

        htmltext = requests.get(url).content
        pageall = re.search(r'"totalPage":(.*?),"currentPage', htmltext).group(1)
        print u'总页数是', pageall
        pagenow = re.search(r'"currentPage":(.*?),"totalCount', htmltext).group(1)
        print u'当前页是', pagenow
        # pagesize = re.search(r'"pageSize":(.*?),"totalPage', htmltext).group(1)
        # print u'pagesize is', pagesize
        totalcount = re.search(r'"totalCount":(.*?)}', htmltext).group(1)
        print u'商品总数是', totalcount
        return '%s,%s,%s' % (pageall, pagenow, totalcount)
        # return pagenum,pagenow,totalcount

    def gettce_sid(url):
        html = requests.get(url).content
        tce_sid1 = re.findall(r'tce_sid&quot;:(\d*)', html)
        tce_sid2 = re.findall(r'"tce_sid":(\d*)}}',html)
        tce_sid = tce_sid1 + tce_sid2
        l2 = list(set(tce_sid))
        l2.remove('')
        print l2
        ids = '%s' % l2[0]
        for i in range(1, l2.__len__()):

            ids = ids + ',%s' % l2[i]
        print ids
        return ids,l2
