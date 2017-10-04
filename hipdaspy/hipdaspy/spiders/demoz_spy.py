# -*- coding: UTF-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from ..items import HipdaspyItem, replyItem
from scrapy.utils.response import *
from scrapy.utils.url import *
import re

class DmozSpider(CrawlSpider):
    name = "hipdaspy"
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://www.hi-pda.com/forum/forumdisplay.php?fid=2",
        "https://www.hi-pda.com/forum/forumdisplay.php?fid=2&page=2"
    ]

    rules = (

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=(r'http://www.hi-pda.com/forum/viewthread.php?tid=\d+')), callback='parse_item'),
    )





    #extract post name info
    def parsePostList(self,response):
        postList = Selector(response).xpath('//*[starts-with(@id, "normalthread_")]/tr/th/span[@id]/a/text()').extract()
        authorList=Selector(response).xpath('//*[starts-with(@id, "normalthread_")]/tr/td[3]/cite/a/text()').extract()
        dateList=Selector(response).xpath('//*[starts-with(@id, "normalthread_")]/tr/td[3]/em/text()').extract()
        linkList = Selector(response).xpath('//*[starts-with(@id, "normalthread_")]//*[starts-with(@id, "thread_")]/a/@href').extract()
        res=[]
        if((len(postList)==len(authorList)) & (len(authorList)==len(dateList))):
            for i in range(len(postList)):
                item=HipdaspyItem()
                item['author']=authorList[i]
                item['title']=postList[i]
                item['postTime']=dateList[i]
                item['link']=linkList[i]
                item['tid']=self.getUrlParm("tid",item['link'])
                res.append(item)
        else:
            print "error author post date list lengeth mismatch"

        return res






    def parsePostContent(self,response):
        selList=Selector(response).xpath('//table[starts-with(@id,"pid")]')
        contentList=[]
        for sel in selList:
            author=sel.xpath('tr')[0].xpath('td/div/a/text()').extract()[0]
            date=sel.xpath('tr')[0].xpath('td//div[@class="authorinfo"]/em/text()').extract()[0]
            content=sel.xpath('tr')[0].xpath('td//div[@class="defaultpost"]//td/text()').extract()[0]

            item=replyItem()
            item['author']=author
            item['postTime']=date
            item['content']=content
            item['tid']=self.getUrlParm("tid",get_base_url(response))
            contentList.append(item)

        pageNum=Selector(response).xpath('//a[@class="next"]')
        nextPageLink=0
        if(len(pageNum)!=0):
            print len(pageNum)
            link=pageNum[0].xpath("@href").extract()[0]
            base_url = get_base_url(response)
            nextPageLink=urljoin_rfc(base_url,link)

        return nextPageLink,contentList


    def parse(self, response):
        res=self.parsePostList(response)

        linkList=[]

        for item in res:
            link=item['link']
            base_url=get_base_url(response)
            linkList.append(urljoin_rfc(base_url,link))
            yield item

        if(len(linkList)==0):
            nextPageLink,cotentList=self.parsePostContent(response)
            for item in cotentList:
                yield item
            if(nextPageLink!=0):
                yield Request(nextPageLink)



        for url in linkList:
            yield Request(url)



    def start_requests(self):
        yield Request(url="https://www.hi-pda.com/forum/logging.php?action=login&sid=5Dzzsp",meta={'cookiejar':1},callback=self.post_login)


    def post_login(self,response):
        print "post login"
        formhash=Selector(response).xpath('//*[@id="loginform"]/input[1]/@value').extract()[0]

        return [FormRequest.from_response(response,  url="https://www.hi-pda.com/forum/logging.php?action=login&loginsubmit=yes&inajax=1",
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          formdata={
                                              'formhash': formhash,
                                              'referer':'https: // www.hi - pda.com / forum / index.php',
                                              'loginfield':'username',
                                              'username':'worenimamai',
                                              'password':'ba81d5fa9a0dea60104bc6ec8175a940',
                                              'questionid':'0',
                                              'answer':'',
                                              'cookietime':'2592000'
                                          },
                                          callback=self.after_login,
                                          dont_filter=True
                                          )]



    def after_login(self,response):
        print "after login"
        cookieList = response.headers.getlist('Set-Cookie')
        cookieDict={}
        for i in range(len(cookieList)):
            print cookieList[i]
            key=cookieList[i].split(";")[0].split("=")[0]
            val=cookieList[i].split(";")[0].split("=")[1]
            cookieDict[key]=val

        print cookieDict
        print response.encoding
        for url in self.start_urls:
            yield Request(url,cookies=cookieDict)



    def getUrlParm(self,parmName,str):
        res=re.findall("[^\?&]?" + parmName + "=[^&]+",str)
        if(len(res)!=0):
            return res[0].split("=")[1]