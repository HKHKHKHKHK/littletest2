# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from littletest.items import liePinItem
from scrapy_redis.spiders import RedisSpider

class Test1Spider(RedisSpider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    # start_urls = ['https://www.liepin.com/shujufenxi']
    redis_key = 'liepin:start_urls'
    basicPage = 'https://www.liepin.com'
    # rules = {
    #     Rule(LinkExtractor(allow='https://www.liepin.com/[a-zA-Z0-9]+/$',deny= "/article/"), follow=True),
    #     Rule(LinkExtractor(allow='/pn\d+/'),  follow=True),
    #     Rule(LinkExtractor(allow='/job/\d+\.shtml'), callback='parse_item', follow=False),
    # }
    #
    # def parse_item(self,response):
    #     item = liePinItem()
    #     item['title'] = response.xpath("//div[@class='title-info']/h1/text()").extract()[0].strip()
    #     item['salary'] = response.xpath("//div/p[@class='job-item-title']/text()").extract()[0].rstrip()
    #     #item['link'] = response.url
    #     print (item['title'], item['salary'] )
    #     yield item
    # #     #yield scrapy.Request(callback = self.parse_item(),meta = {'download_timeout':10})


    def parse(self, response):
        item = liePinItem()
        #item['title'] = response.xpath("//div[@class='job-info']/span[@class='job-name']/@title").extract()
        item['nextPage']=nextPage = response.xpath("//div[@class='pagerbar']/a/@href").extract()[7]
        # item['date'] = response.xpath("//div[@class='cl']/p[@class='authors'/a/text()]").extract()
        # item['author'] = response.xpath("//div[@class='cl']/p[@class='authors'/span/text()").extract()
        print (item['nextPage'])
        yield item
        nextPage = response.xpath("//div[@class='pagerbar']/a/@href").extract()[7]
        yield scrapy.Request(self.basicPage + nextPage,callback = self.parse,meta = {'download_timeout':10},dont_filter=True)

