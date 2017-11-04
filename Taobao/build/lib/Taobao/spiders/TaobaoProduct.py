# -*- coding: utf-8 -*-
import redis
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from Taobao.items import TaobaoProductItem
from Taobao.items import TaobaoItem
from Taobao.items import DetailCategoryItem
from Taobao.items import TmallProductItem
import sys
import requests
import re
import time
pool = redis.ConnectionPool(host='localhost', port='6379')
r = redis.Redis(connection_pool=pool)
reload(sys)
sys.setdefaultencoding('utf-8')

from scrapy_redis.spiders import RedisSpider


class TaobaoProductspider(RedisSpider):


    name = 'taobao'
    redis_key = 'taobao:start_urls'
    # s = raw_input('输入你要爬取的url')
    num = 0
    # 用来保持登录状态，可把chrome上拷贝下来的字符串形式cookie转化成字典形式，粘贴到此处
    # pool = multiprocessing.Pool(multiprocessing.cpu_count())

    cookies = {
        "Cookie": '_med=dw:1536&dh:864&pw:1920&ph:1080&ist:0; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; UM_distinctid=15dca6115246c3-0dfc97a763d484-5393662-144000-15dca611525dd5; lzstat_uv=30787758763010013395|2144678; ali_ab=183.213.204.53.1502368440882.2; _m_h5_tk=952685c13c26d542eb976e2fe6726908_1503752571133; _m_h5_tk_enc=5a3f96f3ac18af3abd21768d3324271c; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; v=0; _tb_token_=5ee7e5133e50e; uc1=cookie14=UoTcC%2B1jzvbevg%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=true&cookie21=UtASsssmfavZrexPkAwn7A%3D%3D&tag=8&cookie15=UtASsssmOIJ0bQ%3D%3D&pas=0; uc3=sg2=B0ADfs%2FnzIHS6UMwzjAdkee1IwxLj1ASW%2Fg09RGSIx8%3D&nk2=3GG9ByzlQxc%3D&id2=UU6jUKD28Q3Szw%3D%3D&vt3=F8dBzWYfWowhqfUJ%2FCA%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; existShop=MTUwNDE1OTc3OA%3D%3D; uss=AQI%2F26KJ3OqWCdGkHBBRaExsAY58SyBBadQoFIqhq66saeyP6%2B4NC8JOFQ%3D%3D; lgc=%5Cu7A7A%5Cu5C71%5Cu5929%5Cu884C; tracknick=%5Cu7A7A%5Cu5C71%5Cu5929%5Cu884C; cookie2=1c214c51fc67ce95a41a3922e5096842; sg=%E8%A1%8C65; mt=np=&ci=6_1&cyk=-1_-1; cookie1=B0T4wBHE8elxtMVYgOOVZSFwJv%2FT5SS5eKH3cJ%2BFZL8%3D; unb=2628644886; skt=a44133d5f70c9c61; t=6cabd2a3c846c7a006bf75959a582abb; _cc_=UIHiLt3xSw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu7A7A%5Cu5C71%5Cu5929%5Cu884C; cookie17=UU6jUKD28Q3Szw%3D%3D; isg=AujoR0QzJSx2RQmNUPMnDMbeudZWBUYdhmMaIaIZQGNW_YlnSyVYqs59g6P2; cna=dooHEt41fAQCAXWILgDWKCHS',
        # "cookie": 'isg=AllZdGtFZONoCTlo1GmcFnLMaUVzYE2YrmiPz3sI2QCMgnsUwjIuaIPa8tkv; cna=YbBNEFiMMBcCAdrNEplmQ/E2; l=AikpDdDqxUCzuahexS3M63DBOd-F-h1b; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cq=ccp%3D1; uss=VvuGgsSH%2FfHAqccJ5UlRnU80uOg59yeYJK8mMuQwOCm%2B%2BcQhujoe0BhGIw%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; um=BA335E4DD2FD504F5AE9F99B98E6EDC2796D9417B0B5DA7A1E9E31DBA3DFFA53F813D5AB69FC9D8CCD43AD3E795C914C553EEB7878ED26221E4C6070FA379441; pnm_cku822=198UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRHlAfkN6QnZLdCI%3D%7CU2xMHDJ%2BH2QJZwBxX39RaVd5WXcrSixAJ1kjDVsN%7CVGhXd1llXGhTbldpVG1VYVxjVGlLc0tySnRBfkd4RXlBdEF1QW85%7CVWldfS0QMAgwCioWKwslVWkMf09%2FW39CMx1LHQ%3D%3D%7CVmhIGCwSMg8vEy0UIAA7BDEMLBAuFS4ONA86GiYYIxg4Aj0IXgg%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; x=__ll%3D-1%26_ato%3D0; tk_trace=1; t=f30bf9df9bae37846e54cfd700da9d64; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BiKmnD2R%2FYH2k%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=3c2f256917427a4ebcdec3bc8bccb495; _tb_token_=3de056306bce3; tt=tmall-main; res=scroll%3A1349*6280-client%3A1349*635-offset%3A1349*6280-screen%3A1366*768; swfstore=78954'
        'cookie': 'thw=cn; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; l=Alpa82K2TT0LI-7Jkcvv-wM8Kg59ut5l; v=0; _m_h5_tk=8f873865614d18f00a6f2cb00a234f45_1496286230748; _m_h5_tk_enc=96ce759cc0828d1b1f348b63e7b6e5f4; _tb_token_=f57e635b63310; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BuSsQxlr4ptL8%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTQ5NjI4MzU5Nw%3D%3D; uss=Vq8%2FLiMpynC3aNoMIum1rAbPzvG%2F4pTeJOpUqetBv55%2B53gnhUGK7NkS8w%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=1c36a9dc87049abbde8fdc4952e71dde; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; skt=050602e5269a263d; t=e8823214ea1fe4e93a65b5419a02f29b; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; cna=VGrXDroWdwACAXAZiUThcFIk; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVLhR&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoW%2BvjaPz%2BAKOQ%3D%3D&tag=8&lng=zh_CN; mt=ci=22_1; isg=Ajk51CfRRAf9rhillXUEhgzJSKXT7pf5-wpUBFtutWDf4ll0o5Y9yKcwENPv',
        'cookie': 'swfstore=84334; thw=cn; cna=YbBNEFiMMBcCAdrNEplmQ/E2; l=Am1tO6FA3sDQE2wS4cHAmWHbfQPlh6GY; isg=Avr6EdeHd0sdfPotC7QP25WZSiDcA1XYaZ0MygTzrw1Y95ox7DvOlcAFMZzw; miid=235384493423096040; t=f30bf9df9bae37846e54cfd700da9d64; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; _cc_=UIHiLt3xSw%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1; um=BA335E4DD2FD504F5AE9F99B98E6EDC2796D9417B0B5DA7A1E9E31DBA3DFFA53F813D5AB69FC9D8CCD43AD3E795C914CF98D06E3BEC51AB74E2CE3B12A4FB038; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51ROidHpo%2FIL4%3D&lg2=URm48syIIVrSKA%3D%3D; uss=VAiW5E3NgBUBdCKcIV%2BHqBBWiqzby95QgK8YakboIjqxTDOgbKgESVy4WQ%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; UM_distinctid=15c0c4d1d8c9f-05c80691656ecb-1263684a-100200-15c0c4d1d8e2b0; mt=np=&ci=21_1; cookie2=3ca4e296ea72230b57f821f40294fd2a; v=0; _tb_token_=39e7d8beb1557; existShop=MTQ5NzI1MTI1Mw%3D%3D; skt=a65277b53f249b8c; whl=-1%260%260%261497251303628; uc1=cookie14=UoW%2Bv%2FZdA7TDCA%3D%3D&lng=zh_CN&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQoVXj&tag=8&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D',
        # "Cookie": 'mt=ci%3D-1_0; miid=507269183165611687; thw=cn; v=0; linezing_session=FYM8EeU9EccengVSNr8WMMmA_1496046290440g5ih_1; _tb_token_=f33e5b55d3eb7; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; _m_h5_tk=a77a0c6a6fe2929b6872a5106c32dc37_1496061088014; _m_h5_tk_enc=ffce0027c84d8dd9828231ed3932a82d; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2Bg2lgc3w74S%2F4%3D&lg2=UtASsssmOIJ0bQ%3D%3D; existShop=MTQ5NjA1ODI3Ng%3D%3D; uss=BdZTFcNZwa2%2FyfMyYpW6luWBEqppobtxy2UZMz9TYAwhoT%2F3aOSr02GIOw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=12b9b92a9842c32511d5d581eba9a475; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; skt=7b88fce95936599d; t=7e0a82ef19012d6337a6404e5c7d2e6b; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; cna=WU/LDq/+tBQCAdrNFG1PPdPe; mt=ci=22_1&cyk=0_0; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=UIHiLt3xThH8t7YQouiW&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoW%2BvjS6JkNylA%3D%3D&tag=8&lng=zh_CN; l=AmNjVymi13MjqgbiC0923iPTc6kNWPea; isg=Ak5OFcrXm5Ve1C7nQheDMXBUnyQizxLJiQ9IEniXutEM2-414F9i2fSZZZpi',
        # "cookie": 'isg=AllZdGtFZONoCTlo1GmcFnLMaUVzYE2YrmiPz3sI2QCMgnsUwjIuaIPa8tkv; cna=YbBNEFiMMBcCAdrNEplmQ/E2; l=AikpDdDqxUCzuahexS3M63DBOd-F-h1b; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cq=ccp%3D1; uss=VvuGgsSH%2FfHAqccJ5UlRnU80uOg59yeYJK8mMuQwOCm%2B%2BcQhujoe0BhGIw%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; um=BA335E4DD2FD504F5AE9F99B98E6EDC2796D9417B0B5DA7A1E9E31DBA3DFFA53F813D5AB69FC9D8CCD43AD3E795C914C553EEB7878ED26221E4C6070FA379441; pnm_cku822=198UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRHlAfkN6QnZLdCI%3D%7CU2xMHDJ%2BH2QJZwBxX39RaVd5WXcrSixAJ1kjDVsN%7CVGhXd1llXGhTbldpVG1VYVxjVGlLc0tySnRBfkd4RXlBdEF1QW85%7CVWldfS0QMAgwCioWKwslVWkMf09%2FW39CMx1LHQ%3D%3D%7CVmhIGCwSMg8vEy0UIAA7BDEMLBAuFS4ONA86GiYYIxg4Aj0IXgg%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; x=__ll%3D-1%26_ato%3D0; tk_trace=1; t=f30bf9df9bae37846e54cfd700da9d64; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BiKmnD2R%2FYH2k%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=3c2f256917427a4ebcdec3bc8bccb495; _tb_token_=3de056306bce3; tt=tmall-main; res=scroll%3A1349*6280-client%3A1349*635-offset%3A1349*6280-screen%3A1366*768; swfstore=78954'
        # 'cookie': 'thw=cn; uc3=nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BkfZRUklsV0HU%3D&lg2=UIHiLt3xD8xYTw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; _cc_=URm48syIZQ%3D%3D; tg=0; mt=ci=-1_0; l=Alpa82K2TT0LI-7Jkcvv-wM8Kg59ut5l; t=e8823214ea1fe4e93a65b5419a02f29b; cookie2=1c36a9dc87049abbde8fdc4952e71dde; v=0; _m_h5_tk=8f873865614d18f00a6f2cb00a234f45_1496286230748; _m_h5_tk_enc=96ce759cc0828d1b1f348b63e7b6e5f4; _tb_token_=f57e635b63310; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; swfstore=157537; JSESSIONID=62B82D070B0DC8A62E19DB2D77DFD5FC; cna=VGrXDroWdwACAXAZiUThcFIk; uc1=cookie14=UoW%2BvjaPz%2BbSDw%3D%3D; isg=AlVVgLIPoLs0HoTxGcGgasiFZFHP-rNlPzboMNf6EUwbLnUgn6IZNGPsjAdj; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0',
        # 'cookie': 'thw=cn; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; l=Alpa82K2TT0LI-7Jkcvv-wM8Kg59ut5l; v=0; _m_h5_tk=8f873865614d18f00a6f2cb00a234f45_1496286230748; _m_h5_tk_enc=96ce759cc0828d1b1f348b63e7b6e5f4; _tb_token_=f57e635b63310; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; uc1=cookie14=UoW%2BvjaPz%2BOStA%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=false&cookie21=URm48syIYB3rzvI4DJOx&tag=8&cookie15=VT5L2FSpMGV7TQ%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BuSsQxlr4ptL8%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTQ5NjI4MzU5Nw%3D%3D; uss=Vq8%2FLiMpynC3aNoMIum1rAbPzvG%2F4pTeJOpUqetBv55%2B53gnhUGK7NkS8w%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=1c36a9dc87049abbde8fdc4952e71dde; sg=%E8%8D%AF49; mt=np=&ci=-1_0; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; skt=050602e5269a263d; t=e8823214ea1fe4e93a65b5419a02f29b; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; cna=VGrXDroWdwACAXAZiUThcFIk; isg=Aiwse9FXWdD7qU3aaDbJ0Wna_QqeTWqOPrnh24ZtOFd6kcybrvWgHyIjxWzS',
        # "Cookie": 'mt=ci%3D-1_0; miid=507269183165611687; thw=cn; v=0; linezing_session=FYM8EeU9EccengVSNr8WMMmA_1496046290440g5ih_1; _tb_token_=f33e5b55d3eb7; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2Bg2xdm%2FnbtrRw%3D&lg2=URm48syIIVrSKA%3D%3D; existShop=MTQ5NjA0OTQyNA%3D%3D; uss=BdZTFcNZwa2%2FyfMyYpW6luWBEqppobtxy2UZMz9TYAwhoT%2F3aOSr02GIOw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=12b9b92a9842c32511d5d581eba9a475; mt=np=&ci=-1_0&cyk=0_0; skt=c97efc7a2956a7a1; t=7e0a82ef19012d6337a6404e5c7d2e6b; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; cna=WU/LDq/+tBQCAdrNFG1PPdPe; l=AlhY8vMbXALMI20jzIaNr/BEqIjrQLzL; isg=AuzsOw-xmZNEYIz5HA3Bd6ZevcrKYpBPP9UqrEYs-hc6UYhbYLVL33LjB4S8',
        #  # "cookie": 'isg=AllZdGtFZONoCTlo1GmcFnLMaUVzYE2YrmiPz3sI2QCMgnsUwjIuaIPa8tkv; cna=YbBNEFiMMBcCAdrNEplmQ/E2; l=AikpDdDqxUCzuahexS3M63DBOd-F-h1b; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cq=ccp%3D1; uss=VvuGgsSH%2FfHAqccJ5UlRnU80uOg59yeYJK8mMuQwOCm%2B%2BcQhujoe0BhGIw%3D%3D; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; um=BA335E4DD2FD504F5AE9F99B98E6EDC2796D9417B0B5DA7A1E9E31DBA3DFFA53F813D5AB69FC9D8CCD43AD3E795C914C553EEB7878ED26221E4C6070FA379441; pnm_cku822=198UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRHlAfkN6QnZLdCI%3D%7CU2xMHDJ%2BH2QJZwBxX39RaVd5WXcrSixAJ1kjDVsN%7CVGhXd1llXGhTbldpVG1VYVxjVGlLc0tySnRBfkd4RXlBdEF1QW85%7CVWldfS0QMAgwCioWKwslVWkMf09%2FW39CMx1LHQ%3D%3D%7CVmhIGCwSMg8vEy0UIAA7BDEMLBAuFS4ONA86GiYYIxg4Aj0IXgg%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; x=__ll%3D-1%26_ato%3D0; tk_trace=1; t=f30bf9df9bae37846e54cfd700da9d64; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BiKmnD2R%2FYH2k%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=3c2f256917427a4ebcdec3bc8bccb495; _tb_token_=3de056306bce3; tt=tmall-main; res=scroll%3A1349*6280-client%3A1349*635-offset%3A1349*6280-screen%3A1366*768; swfstore=78954'
        # 'cookie':'thw=cn; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; l=Alpa82K2TT0LI-7Jkcvv-wM8Kg59ut5l; v=0; _m_h5_tk=8f873865614d18f00a6f2cb00a234f45_1496286230748; _m_h5_tk_enc=96ce759cc0828d1b1f348b63e7b6e5f4; _tb_token_=f57e635b63310; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BuSsQxlr4ptL8%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTQ5NjI4MzU5Nw%3D%3D; uss=Vq8%2FLiMpynC3aNoMIum1rAbPzvG%2F4pTeJOpUqetBv55%2B53gnhUGK7NkS8w%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=1c36a9dc87049abbde8fdc4952e71dde; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; skt=050602e5269a263d; t=e8823214ea1fe4e93a65b5419a02f29b; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; cna=VGrXDroWdwACAXAZiUThcFIk; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVLhR&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoW%2BvjaPz%2BAKOQ%3D%3D&tag=8&lng=zh_CN; mt=ci=22_1; isg=Ajk51CfRRAf9rhillXUEhgzJSKXT7pf5-wpUBFtutWDf4ll0o5Y9yKcwENPv'
        'cookie':'_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2Bv9myKQhOhgoo%3D&lg2=UIHiLt3xD8xYTw%3D%3D; uss=AQZcOa2jL9yJ3SHtl1hEUgRyfUtJBzV8brA7y2ujL%2Fp%2ByVR7O20T6%2F5zfw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; t=7e0a82ef19012d6337a6404e5c7d2e6b; cookie2=3c5e64ca8e7150a03b694d60d16a67fa; _tb_token_=c93967783e57b; pnm_cku822=000UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRH9HcktzSXROdSM%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhTaFBlXGReY1liVWhKfkJ9R3pFcEh1Sn5Lf0d8UgQ%3D%7CVWldfS0QMAo%2FACAePhAgBDkXQRc%3D%7CVmhIGCwWNgsrFykQJAQ%2FAjYIKBQqESoKMAs%2BHiIcJxw8BjkMWgw%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1349*6093-client%3A1349*605-offset%3A1349*6093-screen%3A1366*768; cq=ccp%3D1; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=171655; cna=WU/LDq/+tBQCAdrNFG1PPdPe; isg=Ah0dKF5hGIn5Lv3qpYKgVF9ZLPnXkuuN9vI739_iWXSjlj3Ip4phXOsEtJdF'
    }
    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需
    headers = {
        'Connection': 'keep - alive',
        # 'cookie':'l=And3GVTlBp22J5JeN-taUCSbh2XBPEue; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; _tb_token_=5f35353bae54e; uc1=cookie14=UoW%2BvfJYj9TKrw%3D%3D&lng=zh_CN&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQoVXj&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0; uc3=nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BiKmnGBRRYIeg%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=104dbd98455ee12963862f282ee09523; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; tt=login.tmall.com; pnm_cku822=027UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FR3JKdUp3SXFNeS8%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhQZV1iXWBeZlpuWWRGf0J7T3BOcUlyS35FfkZ%2FQW85%7CVWldfS0TMw8xDjAQJAQqEDoBORwrVCwVO207%7CVmhIGCwWNgsrFyoSKQkzCzIOLhIsFywMNg04GCQaIRo6AD8KXAo%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1056*7541-client%3A1056*605-offset%3A1056*7541-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=251861; whl=-1%260%260%260; cna=WU/LDq/+tBQCAdrNFG1PPdPe; isg=AjY2UQs1c6kZ_AafOp87eahMh2z4_8CQYQcgSqAe5Zm349R9COZ_ofPVj6JZ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        # 'host': ['list.tmall.com','s.taobao.com'],
        'Host': 's.taobao.com',
        # 'authority':'chi.taobao.com',
        'upgrade - insecure - requests': '1',
        # 'path': '/itemlist/huichi2014.htm?cat=50002766%2C50035978%2C50008825%2C50042258%2C50103282%2C50103280%2C50106154%2C50108542&user_type=0&at=45634&viewIndex=1&as=0&spm=a219e.8128116.chiNav.3.CPlzEL&atype=b&style=grid&q=%E4%BC%91%E9%97%B2%E9%9B%B6%E9%A3%9F&same_info=1&tid=0&isnew=2&_input_charset=utf-8'
    }
    cookies2 = {
        'cookie': '_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=171655; _tb_token_=c93967783e57b; uc1=cookie14=UoW%2BvjJihio6EA%3D%3D&lng=zh_CN&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV5%2FHr5SeW%2F599U%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; uss=UUoy1aH74%2FcAnguKjbBDNTJVGZXPOncThccMMuBFF6HNDfCr%2FInq42YM6g%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=3c5e64ca8e7150a03b694d60d16a67fa; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=179UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRH9HckZ%2FQnZNciQ%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhTaFBlUWhVYVplUm9NdEt%2FQHhHfEd8RXpGeUd%2BRWs9%7CVWldfS0RMQ0zBzgYJBk5FzcOLhI3YUUoTTMdSx0%3D%7CVmhIGCwWNgsrHiIWNgwzCDwcIB4lHj4EPwoqFigTKAgyDThuOA%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A990*7269-client%3A819*588-offset%3A819*7269-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=ArS040OBUdL-p8RRFBWZXz62hXLmJWJ2ty3iBE4VQD_CuVQDdp2oB2p7Tey0'
    }
    headers2 = {
        # 'Connection': 'keep - alive',
        # 'cookie':'l=And3GVTlBp22J5JeN-taUCSbh2XBPEue; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; _tb_token_=5f35353bae54e; uc1=cookie14=UoW%2BvfJYj9TKrw%3D%3D&lng=zh_CN&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQoVXj&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0; uc3=nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BiKmnGBRRYIeg%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=104dbd98455ee12963862f282ee09523; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; tt=login.tmall.com; pnm_cku822=027UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FR3JKdUp3SXFNeS8%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhQZV1iXWBeZlpuWWRGf0J7T3BOcUlyS35FfkZ%2FQW85%7CVWldfS0TMw8xDjAQJAQqEDoBORwrVCwVO207%7CVmhIGCwWNgsrFyoSKQkzCzIOLhIsFywMNg04GCQaIRo6AD8KXAo%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1056*7541-client%3A1056*605-offset%3A1056*7541-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=251861; whl=-1%260%260%260; cna=WU/LDq/+tBQCAdrNFG1PPdPe; isg=AjY2UQs1c6kZ_AafOp87eahMh2z4_8CQYQcgSqAe5Zm349R9COZ_ofPVj6JZ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        # 'host': ['list.tmall.com','s.taobao.com'],
        'authority': 'list.tmall.com',
        'upgrade - insecure - requests': '1',
        'accept-language':'zh-CN,zh;q=0.8',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'path':'/search_product.htm?spm=875.7931836/B.subpannel2016028.23.ck9oPp&q=%BC%D0%BF%CB&pos=1&cat=50025174&active=1&style=g&from=sn_1_rightnav&acm=201603072.1003.2.708738&sort=s&search_condition=7&scm=1003.2.201603072.OTHER_1485484270863_708738&smToken=9fea5c5e10c24d9395ff4ee6166b5ee2&smSign=KUPS9phNeEbFXol5V1TJVg%3D%3D',
        'cache-control':'max-age=0'
        # 'path': '/itemlist/huichi2014.htm?cat=50002766%2C50035978%2C50008825%2C50042258%2C50103282%2C50103280%2C50106154%2C50108542&user_type=0&at=45634&viewIndex=1&as=0&spm=a219e.8128116.chiNav.3.CPlzEL&atype=b&style=grid&q=%E4%BC%91%E9%97%B2%E9%9B%B6%E9%A3%9F&same_info=1&tid=0&isnew=2&_input_charset=utf-8'
    }
    cookies3 = {
        'cookie': 'swfstore=81254; miid=507269183165611687; thw=cn; l=Ap6eIfgkovAmJWsx9ijj/I7ebjrgy2LZ; _m_h5_tk=2ed9243d92afc7587999a5e01734ffdd_1496933558507; _m_h5_tk_enc=ec88863b77b60d8b1ad6217a1ab2aac3; v=0; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZdA7%2FuxA%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4plD&tag=8&cookie15=URm48syIIVrSKA%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51ROiWXLf5I%2FU%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTQ5NzI1MTk5Mw%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; mt=np=&ci=22_1&cyk=3_0; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; skt=ef548fae40121619; t=7e0a82ef19012d6337a6404e5c7d2e6b; _cc_=WqG3DMC9EA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; cna=WU/LDq/+tBQCAdrNFG1PPdPe; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%261497252410650; isg=AgMDdr94XlSDARPkzwAm4oU7ksdt0C27fJBVUTXgX2LZ9CMWvUgnCuFuGplv',
        'cookie': 'swfstore=81254; miid=507269183165611687; thw=cn; l=Ap6eIfgkovAmJWsx9ijj/I7ebjrgy2LZ; _m_h5_tk=2ed9243d92afc7587999a5e01734ffdd_1496933558507; _m_h5_tk_enc=ec88863b77b60d8b1ad6217a1ab2aac3; v=0; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZdA7%2FuxA%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4plD&tag=8&cookie15=URm48syIIVrSKA%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51ROiWXLf5I%2FU%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTQ5NzI1MTk5Mw%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; mt=np=&ci=22_1&cyk=3_0; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; skt=ef548fae40121619; t=7e0a82ef19012d6337a6404e5c7d2e6b; _cc_=WqG3DMC9EA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; cna=WU/LDq/+tBQCAdrNFG1PPdPe; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%261497252494431; isg=AnZ2nZqbM_9-xMZf-t_7OWiMx6y4PwDQoUdgiuBfY9n0Ixa9SCcK4dzZT-Ka'
    }

    cookies4 = {
        'cookie':'_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=249201; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZeeFqgcQ%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51Rq6%2FNrmhSY8%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; tt=sec.taobao.com; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=117UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAfUVxTHRAdSM%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhSbVdqUmZbY1diVWhKckdySH1EcE15RXhNdk5wSmQy%7CVWldfS0SMg04DS0RLg4gVWhUalVrTmdcYkdiTBpM%7CVmhIGCwWNgsrESoUNA4xDzQUKBYtFjYMNwIiHiAbIAA6BTBmMA%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A990*7236-client%3A763*588-offset%3A763*7236-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=Ao2N2IE56FIyCk061dJQpE9pnKnHwkI95gKrr88SySSTxq14l7rRDNtcREd1',
        'cookie':'_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=249201; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZeeFqgcQ%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51Rq6%2FNrmhSY8%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; tt=sec.taobao.com; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=111UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAekN8R3pFfCo%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhSbVdtVGtQbVJrXGFDf0p%2BR3pAeEB4Q39LdEx1T2E3%7CVWldfS0QMAsxDy8TJgYoVHMAcwk%2FSypEYBAsSToKOh4jDVsN%7CVmhIGCwWNgsrFykQJAQ%2FAjwBIR0jGCMDOQI3FysVLhU1DzAFUwU%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1349*6030-client%3A1349*605-offset%3A1349*6030-screen%3A1366*768; isg=Ajg4V0rklaUNBvhlyIldE5piCeYKCR8qU5n-EHKphHMmjdh3GrFsu06vMZjo',
        'cookie':'_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=AoWF8jj8lNdQwaDEeSVox-uvFc-/QjnU; swfstore=249201; _tb_token_=e631ee6a83057; uc1=cookie14=UoW%2Bv%2FZeeFqgcQ%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreKQgf&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51Rq6%2FNrmhSY8%3D&lg2=W5iHLLyFOGW7aA%3D%3D; uss=BxJC0EJEBQHN%2FYNUN%2FdrkD00SmmC4TK7rlNDX7cn97KQHp9fclW%2FkDNAMw%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=31acab99370794f23890ce4b0243e4c8; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=7e0a82ef19012d6337a6404e5c7d2e6b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; cq=ccp%3D0; cna=WU/LDq/+tBQCAdrNFG1PPdPe; pnm_cku822=075UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAekN9QX9KcSc%3D%7CU2xMHDJ7G2AHYg8hAS8WLgAgDlIzVTleIFp0InQ%3D%7CVGhXd1llXGhSbVdtVGpWaF1mUWxOcUlzT3JLckxwSHRIfUN6RX5QBg%3D%3D%7CVWldfS0SMg4wDS0VNRswEC8PMB5IHg%3D%3D%7CVmhIGCwWNgsrESoUNA4xDDcXKxUuFTUPNAEhHSMYIwM5BjNlMw%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A990*7206-client%3A763*588-offset%3A763*7206-screen%3A1366*768; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=Ai0t-BmNCLL_K-0aNfKwhO-JPMlnIuJdRiJLj28yA0Qz5k2YN9pxLHv0pKfV',
        'cookie':'_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; x=__ll%3D-1%26_ato%3D0; l=ArCw4tCemYbgtfSHX3n13WUuAHABEpRK; _tb_token_=7c7c103738e7; uc1=cookie14=UoW%2Bv%2FZf7Aod8g%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=Vq8l%2BKCLjhS4UhJVbCU7&tag=8&cookie15=URm48syIIVrSKA%3D%3D&pas=0; uc3=sg2=VFIf3Zbm%2FPzM6VKXOipPo%2BRjA8np8E8SQ%2FogbNtphTA%3D&nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV51RzG9N6wxayE%3D&lg2=URm48syIIVrSKA%3D%3D; uss=U7PCzlBnZyD0Ajm09IOMPBOwnivCPLuM7eQpVmberdPQ%2BqZYAIL1Ytt3TA%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=10b75e1acc8da7caaee0058b116d26ef; sg=%E8%8D%AF49; cookie1=B0T4m12SYtAkfF25EJaj8C3fvMnt9CO8CLvSA4Q2tNo%3D; unb=2661237324; t=e8823214ea1fe4e93a65b5419a02f29b; _l_g_=Ug%3D%3D; _nk_=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie17=UU6nQPq3aLby9w%3D%3D; login=true; tt=login.tmall.com; cna=VGrXDroWdwACAXAZiUThcFIk; pnm_cku822=166UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FRXpAdUhxTnNOcyU%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhSbVdiX2ZZZFlkU25MeEdyR39LdEt3QnhEeU12TmA2%7CVWldfS0SMg04DCwQJAQqFysVKhQxGCMdOB1vEkIpf09kM2RKHEo%3D%7CVmhIGCUFOBgkGiMXNwwxCjcXKxUuFTUPNAEhHSMYIwM5BjNlMw%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D; res=scroll%3A1349*6060-client%3A1349*662-offset%3A1349*6060-screen%3A1366*768; cq=ccp%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=23207; whl=-1%260%260%260; isg=AszMm7mH-SGExuwbaQZG4Q8znSo-rVvy2r--zSaN23casWy7ThVAP8IDJY9y'
    }
    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
    # pageres = None, resurl = None, resurl2 = None,
    def __init__(self,isTaobao=None,isdataSource=None,isapiData=None,pageres = None, resurl = None, resurl2 = None,start_url=None,wantpage=None,dataurl=None, *args, **kwargs):
        super(TaobaoProductspider, self).__init__(*args, **kwargs)
        self.isTaobao = r.get('tb_isTaobao')
        self.isdataSource = r.get('tb_isdataSource')
        self.isapiData = r.get('tb_isapiData')
        self.pageres = r.get('tb_pageres')
        self.resurl = r.get('tb_resurl')
        self.resurl2 = r.get('tb_resurl2')
        self.start_url = r.get('tb_url')
        self.Tbwantpage = r.get('tb_wantpage')
        self.dataurl = r.get('tb_dataurl')
        #s = raw_input('111')

    def start_requests(self):
        self.start_urls.append(self.start_url)
        for eachurl in self.start_urls:
            if self.isTaobao=='1':
                #判断数据来源
                html = requests.get(eachurl)
                selector = Selector(html)
                if self.isdataSource == '1':
                    #print u'该页面数据来源于页面源代码'

                    yield Request(url = eachurl,callback=self.parse)
                else:
                    #print u'该页面的数据来源于ajax'
                    #从页面源代码获取数据页面的参数
                    if self.isapiData=='1':
                        # paras = selector.xpath('//input[@id="J_FirstAPI"]/@value').extract()[0]
                        # print 'paras is',paras
                        # dataurl = "https://list.taobao.com/itemlist/acg.htm?_input_charset=utf-8&json=on&%s"%paras
                        # print dataurl
                        yield Request(url = self.dataurl,callback=self.getajaxdata,cookies=self.cookies3,meta={'url':self.dataurl})
                        # self.getajaxdata(dataurl)
                    else:
                        # tce_sid = self.gettce_sid(eachurl)
                        # newurl = 'https://tce.taobao.com/api/mget.htm?tce_sid=%s'%tce_sid[0]
                        # print newurl
                        yield Request(url=self.resurl,callback=self.geturlsBytce_sid,cookies=self.cookies)
                        for eachresurl in self.resurl2.split(','):
                            # newurl2 = 'https://www.taobao.com/go/rgn/sys/xctrl/dispatch.php?murl=http://tce.taobao.com/api/get.htm&tce_sid=%s' % eachsid
                            yield Request(url = eachresurl,callback=self.geturlsBytce_sid,cookies=self.cookies)
                    # self.getUrlsByAjax(dataurl)
            else:
                #print u'该页面是天猫页面'
                # html = requests.get(eachurl,cookies=self.cookies4)
                # print html.content
                # selector = Selector(html)
                # pageall = selector.xpath('//input[@name="totalPage"]/@value').extract()[0]
                # pagenow = selector.xpath('//input[@name="jumpto"]/@value').extract()[0]
                # print u'该类商品共有',pageall,u'页',u'当前页是',pagenow,u'页'
                # wantpage = raw_input('请输入你想爬到的页数')
                self.wantpage = self.Tbwantpage
                # yield self.parse_tmalllist(html)
                yield Request(url=eachurl,callback=self.parse_tmalllist,dont_filter=True,cookies=self.cookies,meta={'url':eachurl})
                # yield Request(url = )
                # dataurl =

    def getajaxdata(self,response):
        url = response.meta['url']
        str = requests.get(url, cookies=self.cookies3).content

        alldata = re.findall(r'"image":(.*?)"spSource"', str,re.S)
        #print 'the length is',alldata.__len__()
        for eachdata in alldata:

            id = re.search(r'"itemId":"(\d*)"', eachdata).group(1)
            price = re.search(r'"price": "(\d*\.\d*)"', eachdata, re.S).group(1)
            actualprice = re.search(r'"currentPrice":"(\d*\.\d*)"', eachdata, re.S).group(1)
            url = 'https://item.taobao.com/item.htm?id=%s' % id
            # name = re.search(r'"title":"(.*?)", "price":',eachdata,re.S).group(1)
            sellerlink = re.search(r'"storeLink":"(.*?)",', eachdata).group(1)
            sellernick = re.search(r'"nick":"(.*?)",', eachdata).group(1).decode('gb18030').encode('utf8')
            yield Request(url=url, callback=self.parse_TaobaoProduct2,
                          meta={'id': id, 'price': price, 'actualprice': actualprice, 'sellerlink': sellerlink,
                                'sellerNick': sellernick})

            # yield Request(callback=self.getUrlsByAjax2,meta={'str':str})


    def getPageinfo(self,url):

        htmltext = requests.get(url).content
        pagenum = re.search(r'"totalPage":(.*?),"currentPage', htmltext).group(1)
        #print u'总页数是', pagenum
        pagenow = re.search(r'"currentPage":(.*?),"totalCount', htmltext).group(1)
        #print u'当前页是', pagenow
        pagesize = re.search(r'"pageSize":(.*?),"totalPage', htmltext).group(1)
        #print u'pagesize is', pagesize
        totalcount = re.search(r'"totalCount":(.*?)}', htmltext).group(1)
        #print u'商品总数是', totalcount
        self.Tbwantpage = raw_input('请输入你要爬到的页数')#该参数由前端页面返回
        #print 'self.tbwantpage is',self.Tbwantpage


    def getReadyUrls(self,url):
        Tmallurls = []
        Taobaourls =[]
        htmltext = requests.get(url).content
        pagenow = re.search(r'"currentPage":(.*?),"totalCount', htmltext).group(1)
        #print u'当前页是', pagenow
        jsondatas = re.search(r'"auctions":(.*?),"recommendAuctions"', htmltext).group(1)
        # print jsondatas
        eachitemdata = re.findall(r'"p4pTags"(.*?)"delivery"', jsondatas)
        for eachdata in eachitemdata:
            item = dict()
            #print eachdata
            product_id = re.search(r'"nid":"(.*?)","category"', eachdata).group(1)
            item['id'] = product_id
            try:
                isTmall = re.search(r'isTmall":(.*?),', eachdata).group(1)
            except:
                isTmall = 'false'
            # print isTmall
            if isTmall == 'true':
                item_url = 'https://detail.tmall.com/item.htm?id=%s' % product_id
                item['url'] = item_url
                # print item_url
                Tmallurls.append(item)
                # yield Request(url=item_url, callback=self.parse_Tmallproduct)
            elif isTmall == 'false':
                item_url = 'https://item.taobao.com/item.htm?id=%s' % product_id
                item['url'] = item_url
                # print item_url
                Taobaourls.append(item)
     #返回天猫和淘宝的商品url
        return Tmallurls,Taobaourls,pagenow




    # 页面数据来自ajax,获取商品的信息和url
    def getUrlsByAjax(self,response):
        #print u'进入ajax数据页面'
        # html = requests.get(response.url).content
        alldata = re.findall(r'"image":(.*?)"spSource"',response.body)
        for eachdata in alldata:
            # id = re.search(r'"itemId":"(.*?)", "isLimitPromotion"',eachdata).group(1)
            # price = re.search(r'"price": "(.*?)", "currentPrice',eachdata).group(1)
            # actualpricr = re.search(r'"currentPrice":"(.*?)", "vipPrice',eachdata).group(1)
            # url = re.search(r'"href":"(.*?)", "commend',eachdata).group(1)
            # name = re.search(r'"title":"(.*?)", "price',eachdata).group(1)
            # sellerlink = re.search(r'"storeLink":"(.*?)", "href"',eachdata).group(1)
            # sellernick = re.search(r'"nick":"(.*?)", "sellerId"',eachdata).group(1)
            id = re.search(r'"itemId":"(\d*)"', eachdata).group(1)
            price = re.search(r'"price": "(\d*\.\d*)"', eachdata, re.S).group(1)
            actualprice = re.search(r'"currentPrice":"(\d*\.\d*)"', eachdata, re.S).group(1)
            url = 'https://item.taobao.com/item.htm?id=%s' % id
            # name = re.search(r'"title":"(.*?)", "price":',eachdata,re.S).group(1)
            sellerlink = re.search(r'"storeLink":"(.*?)",', eachdata).group(1)
            sellernick = re.search(r'"nick":"(.*?)",', eachdata).group(1)
            yield Request(url = url,callback=self.parse_TaobaoProduct2,meta={'id':id,'price':price,'actualprice':actualprice,'sellerlink':sellerlink,'sellernick':sellernick})


    def gettce_sid(self,url):
        html = requests.get(url).content
        tce_sid1 = re.findall(r'tce_sid&quot;:(\d*)', html)
        tce_sid2 = re.findall(r'"tce_sid":(\d*)}}',html)
        tce_sid = tce_sid1 + tce_sid2
        l2 = list(set(tce_sid))
        ids = '%s' % l2[0]
        for i in range(1, l2.__len__() - 1):
            ids = ids + ',%s' % l2[i]
        #print ids
        return ids,l2

    #主题页面的商品通过tce_sid返回json数据
    def geturlsBytce_sid(self,response):
        # print response.body
        # html = requests.get(response.url,cookies=self.cookies).content
        try:
            ids = re.findall(r'"auction_id":"(\d*)","item_pic"',response.body)
            ids2 = re.findall(r'"itemId":(\d*),"',response.body)
            # urls = re.findall(r'item_url:"(.*)","', response.body)
            ids3 = re.findall(r'"item_url":"//item.taobao.com/item.htm\?scm=.*?&pvid=.*?&id=(\d*)"', response.body, re.S)
            ids4 = re.findall(r'"item_numiid":"(\d*)"',response.body)
            ids = ids + ids2 +ids3 + ids4
            for eachid in ids:
                url = 'https://item.taobao.com/item.htm?id=%s' % eachid
                #print url
                yield Request(url=url,callback=self.parse_Taobaoproduct,cookies=self.cookies,dont_filter=True,meta={'product_id':eachid})
        except:
            urls = re.findall(r'item_url:"(.*)","', response.body)


    def parse_tmalllist(self,response):
        #print u'我是来解析天猫商品的'
        html = requests.get(response.meta['url'],cookies=self.cookies4)
        # print html.content
        # s = raw_input('aaa')

        selector = Selector(html)
        # htmltext = requests.get(response.url).content
        pagenow = selector.xpath('//input[@name="jumpto"]/@value').extract()[0]
        allGoods = selector.xpath('//div[@class="product  "]')
        for eachGoods in allGoods:
            # try:
            try:
                title = eachGoods.xpath('div/p[@class="productTitle"]/a/text()').extract()[0].encode('utf-8').decode('utf-8')
            except:
                title = eachGoods.xpath('div/div[@class="productTitle productTitle-spu"]/a/text()').extract()[0].encode('utf-8').decode('utf-8')
            #print title
            # title = eachGoods.xpath('div[@class="product-iWrap"]/p[@class="productTitle"]/a/text()')[0].encode('utf-8').decode('utf-8')
            id = eachGoods.xpath('@data-id').extract()[0]
            price = eachGoods.xpath('div/p[@class="productPrice"]/em/@title').extract()[0]
            url = 'https://detail.tmall.com/item.htm?id=%s'%id
            try:
                num = eachGoods.xpath('div/p[@class="productStatus"]/span[1]/em[1]/text()').extract()[0]
            except:
                num = ''
            try:
                allcount = eachGoods.xpath('div[@class="product-iWrap"]/p[@class="productStatus"]/span[2]/a/text()').extract()[0]
            except:
                sellerhref = eachGoods.xpath('div/div[@class="productShop"]/a/@href').extract()[0]
                sellerid = re.search(r'user_number_id=(\d*)&',sellerhref).group(1)
                allcount = self.getallcountByid(sellerid,id)
            # print title+'--'+id+'--'+price+'--'+url+'--'+num+'--'+allcount//*[@id="J_ItemList"]/div[3]/div/p[3]/span[1]/em
            yield Request(url = url,callback=self.parse_Tmallproduct,meta={'title':title,'id':id,'price':price,'num':num,'allcount':allcount})
            # except Exception as e:
            #     print u'跳过该海报商品'
            #     print e

        if pagenow<self.wantpage:
            nexturl = selector.xpath('//a[@class="ui-page-next"]/@href').extract()[0]
            nexturl = 'https://list.tmall.com/search_product.htm%s'%nexturl
            yield Request(url=nexturl,callback=self.parse_tmalllist,dont_filter=True,cookies=self.cookies4,meta={'url':nexturl})
            #print u'self.num is',self.num

    #该方法用于通过sellerid和商品id获取商品的评论总数
    def getallcountByid(self,sellerid,id):
        url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s&sellerId=%s'%(id,sellerid)
        html = requests.get(url).content
        return re.search(r'"rateTotal":(\d*),"',html).group(1)


    #该方法用于构造淘宝数据来源于源代码情况下的下一页的链接构造
    def getNextpageurl(self,nowurl,pagenow):
        if pagenow == 1:
            newurl = nowurl+'&s=60'
            return newurl
        else:
            a = re.search(r'&s=\d*', nowurl).group()
            nextnum = pagenow  * 60
            newurl = nowurl.replace(a, '&s=%d' % nextnum)
            #print u'the nexturl is',newurl
            return newurl

    def parse(self, response):
        selector = Selector(response)
        htmltext = requests.get(response.url).content
        try:
            urls = self.getReadyUrls(response.url)
            Tmallurls = urls[0]
            Taobaourls = urls[1]
            # print Tmallurls,Taobaourls
            #print 'pagenow is',urls[2]
            for eachTmallurl in Tmallurls:
                yield Request(url = eachTmallurl['url'],callback=self.parse_Tmallproduct,meta={'product_id':eachTmallurl['id']})
            for eachTaobaourl in Taobaourls:
                yield Request(url = eachTaobaourl['url'],callback=self.parse_Taobaoproduct,meta={'product_id':eachTaobaourl['id']})
            if int(urls[2]) < int(self.Tbwantpage):
                nexturl = self.getNextpageurl(response.url,int(urls[2]))
                yield Request(url = nexturl,callback=self.parse,cookies=self.cookies)

        except:
            jsondatas = re.search(r'"data":{"spus":(.*?)"spucombo":',htmltext).group(1)
            allitemdata = re.findall(r'"num"(.*?)ag_info"', jsondatas)
            pagenow = re.search(r'"currentPage":(.*?),"totalCount', htmltext).group(1)
            for eachdata in allitemdata:
                #直接获取具体同类商品页面的链接
                # category = re.search(r'":"(.*?)","title"',eachdata).group(1)
                # spu_title = re.search(r'"title":"(.*?)","pic_url"',eachdata).group(1)
                dataurl = re.search(r'"url":"(.*?)","t',eachdata).group(1)
                dataurl = dataurl.replace('\u0026','&').replace('\u003d','=')
                #print dataurl
                yield Request(url ='https://'+ dataurl,callback=self.parse_same_list)

            if int(pagenow) < int(self.Tbwantpage):
                nexturl = self.getNextpageurl(response.url, int(pagenow))
                yield Request(url=nexturl, callback=self.parse, cookies=self.cookies)



                    # print jsondatas
    def getPricefromurl(self,url,id):
        # print 'the priceurl is',url
        # print 'the id is',id
        headers = {
            "cookie": "_m_h5_tk=37bdcb73d755e3669b04693030305793_1495617483456; _m_h5_tk_enc=d016d727ab8efe0afb7d54c366b9e9ff; v=0; _tb_token_=c3cde55156e77; uc3=nk2=r6%2F1cL0I9NPAnA%3D%3D&id2=UU6nQPq3aLby9w%3D%3D&vt3=F8dARV%2BkfZRUklsV0HU%3D&lg2=UIHiLt3xD8xYTw%3D%3D; existShop=MTQ5NTY3ODYyOA%3D%3D; lgc=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; tracknick=%5Cu94C1%5Cu9A6C%5Cu548C%5Cu70B8%5Cu836F; cookie2=1c7a712615fdf9ddaec4a312e459005c; skt=a05a8403a2149870; t=e8823214ea1fe4e93a65b5419a02f29b; _cc_=URm48syIZQ%3D%3D; tg=0; linezing_session=ItzK2Otv4Dhx8X1Yc0ZNAq8a_1495679668980F7aS_2; mt=ci=-1_0; cna=VGrXDroWdwACAXAZiUThcFIk; uc1=cookie14=UoW%2BvfyoklQJGA%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; l=An9/AAVpgN5WtKuaBPTS-PZUj10JdtMG; isg=Ag0NWNh1aMqoyszZ4SmYwsCtHCn4GUG8Jy6gGE-SW6QTRi34FzpRjFvUxm_b",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            'authority': 'detailskip.taobao.com',
            'referer': 'https://item.taobao.com/item.htm?id=%s'%id
        }
        s = requests.get(url, headers=headers)
        # print s.content
        try:
            price = re.search(r'"price":"(\d*\.\d*)","start":false', s.content).group(1)
        except:
            try:
                price = re.search(r'"price":"(.*?)","contract', s.content).group(1)
            except:
                price = re.search(r'"price":"(.*?)","tradeContract"', s.content).group(1)
                
        return price

    def getDetailCount(self,url):
        data = requests.get(url).content
        counts = []
        counts.append(re.search(r'"total":(.*?),"tryRepor', data).group(1))
        counts.append(re.search(r'"goodFull":(.*?),"additiona', data).group(1))

        counts.append(re.search(r'"normal":(.*?),"hascon', data).group(1))
        counts.append(re.search(r'"bad":(.*?),"totalFull', data).group(1))
        counts.append(re.search(r'"additional":(.*?),"correspo', data).group(1))
        return counts

    def parse_Tmallproduct(self,response):
        #print u'this is tmall'
        #将已经获得的属性填入item中
        TmallItem = TmallProductItem()

        TmallItem['product_name'] = response.meta['title']
        TmallItem['product_id'] = response.meta['id']
        TmallItem['product_url'] = response.url
        TmallItem['Price'] = response.meta['price']
        TmallItem['num'] = response.meta['num']
        TmallItem['CommentCount'] = response.meta['allcount']

        selector = Selector(response)
        try:
            TmallItem['defaultPrice'] = re.search(r'"defaultItemPrice":"(\d*\.\d*)"',response.body).group(1)
        except:
            TmallItem['defaultPrice'] = TmallItem['Price']

        TmallItem['sellerName'] = selector.xpath('//input[@name="seller_nickname"]/@value').extract()[0]
        TmallItem['seller_link'] = selector.xpath('//a[@class="slogo-shopname"]/@href').extract()[0]

        yield TmallItem


    def parse_Taobaoproduct(self,response):
        #print u'this is taobao'
        selector = Selector(response)
        htmltext = requests.get(response.url).content
        item = TaobaoProductItem()
        item['product_name'] = selector.xpath('//div[@id="J_Title"]/h3/text()').extract()[0]
        # print 'product_name is',item['product_name']
        item['product_url'] = response.url
        # print 'url is',item['product_url']
        item['product_id'] = response.meta['product_id']
        # print 'product_id is',item['product_id']
        item['Price'] = selector.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()[0]
        # print 'price is ',item['Price']

        priceurldatas = re.search(r"sib.htm\?(.*?)',",htmltext).group(1)
        #构造实际价格的url
        priceurl = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?%s'%priceurldatas
        # print priceurl
        item['ActualPrice'] = self.getPricefromurl(priceurl,item['product_id'])
        # print 'the actual price is',item['ActualPrice']

        # item['sellerid'] = re.search(r'sellerId=(\d*)&modules',priceurldatas).group(1)
        # item['sellerlink'] = re.search(r"url : '(.*?)'",re.search(r"shop  : {(.*?)vdata :{",htmltext).group(1)).group(1)

        shopdata = re.search(r"shop  : {(.*?)vdata", htmltext, re.S).group(1)
        item['sellerlink'] = re.search(r"url : '(.*?)'", shopdata).group(1)

         # sellerNick: '梦倩的衣柜'
        item['sellerNick'] = re.search(r"sellerNick       : '(.*?)'",htmltext).group(1).decode('gbk')
        # print item['sellerid'],item['sellerNick'].decode('gbk')

        commenturl = 'https://rate.taobao.com/detailCommon.htm?auctionNumId=%s'%item['product_id']
        detailCount = self.getDetailCount(commenturl)
        item['AllCount'] =detailCount[0]
        item['GoodCount'] = detailCount[1]
        item['GeneralCount'] =detailCount[2]
        item['PoorCount'] = detailCount[3]
        item['AfterCount'] = detailCount[4]


        yield item


    def parse_TaobaoProduct2(self,response):
        selector = Selector(response)
        htmltext = requests.get(response.url).content
        item = TaobaoProductItem()
        item['product_url'] = response.url
        item['product_name'] = selector.xpath('//h3[@class="tb-main-title"]/text()').extract()[0]
        item['product_id'] = response.meta['id']
        item['Price'] = response.meta['price']
        item['ActualPrice'] = response.meta['actualprice']
        item['sellerlink'] = response.meta['sellerlink']
        item['sellerNick'] = response.meta['sellerNick']

        commenturl = 'https://rate.taobao.com/detailCommon.htm?auctionNumId=%s' % item['product_id']

        detailCount = self.getDetailCount(commenturl)
        item['AllCount'] = detailCount[0]
        item['GoodCount'] = detailCount[1]
        item['GeneralCount'] = detailCount[2]
        item['PoorCount'] = detailCount[3]
        item['AfterCount'] = detailCount[4]

        yield item


#用来解析同类商品在多个店铺售卖的页面
    def parse_same_list(self,response):
        #print u'this samelist'
        urls = self.getReadyUrls(response.url)
        Tmallurls = urls[0]
        Taobaourls = urls[1]
        # print Tmallurls,Taobaourls
        for eachTmallurl in Tmallurls:
            yield Request(url=eachTmallurl['url'], callback=self.parse_Tmallproduct,
                          meta={'product_id': eachTmallurl['id']})
        for eachTaobaourl in Taobaourls:
            yield Request(url=eachTaobaourl['url'], callback=self.parse_Taobaoproduct,
                          meta={'product_id': eachTaobaourl['id']})



    # 该方法用于构造同种商品页面淘宝数据来源于源代码情况下的下一页的链接构造
    def getNextpageAjaxurl(self, nowurl, pagenow):
        if pagenow == 1:
           newurl = nowurl+'&s=44'
           return newurl
        else:
            a = re.search(r'&s=\d*', nowurl).group()
        # print a.group()
            nextnum = pagenow * 44
            newurl = nowurl.replace(a, '&s=%d' % nextnum)
            #print u'the nexturl is', newurl
            return newurl

