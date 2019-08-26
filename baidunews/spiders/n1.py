# -*- coding: utf-8 -*-
import scrapy
from baidunews.items import BaidunewsItem #从核心目录
from scrapy.http import Request
import re
import time
class N1Spider(scrapy.Spider):
    name = 'n1'
    allowed_domains = ['baidu.com']
    start_urls = ["http://news.baidu.com/widget?id=LocalNews&ajax=json"]
    allid=['LocalNews', 'civilnews', 'InternationalNews', 'EnterNews', 'SportNews', 'FinanceNews', 'TechNews', 'MilitaryNews', 'InternetNews', 'DiscoveryNews', 'LadyNews', 'HealthNews', 'PicWall']
    allurl=[]
    for k in range(len(allid)):
        thisurl="http://news.baidu.com/widget?id="+allid[k]+"&ajax=json"
        allurl.append(thisurl)

    def parse(self, response):
        while True: #每隔5分钟爬一次
            for m in range(len(self.allurl)):
                yield Request(self.allurl[m], callback=self.next)
                time.sleep(300) #单位为秒
    cnt=0
    def next(self,response):
        print("第" + str(self.cnt) + "个栏目")
        self.cnt+=1
        data=response.body.decode("utf-8","ignore")
        pat1='"m_url":"(.*?)"'
        pat2='"url":"(.*?)"'
        url1=re.compile(pat1,re.S).findall(data)
        url2=re.compile(pat2,re.S).findall(data)
        if(len(url1)!=0):
            url=url1
        else :
            url=url2
        for i in range(len(url)):
            thisurl=re.sub("\\\/","/",url[i])
            print(thisurl)
            yield Request(thisurl,callback=self.next2)
    def next2(self,response):
        item=BaidunewsItem()
        item["link"]=response.url
        item["title"]=response.xpath("/html/head/title/text()")
        item["content"]=response.body
        print(item)
        yield item