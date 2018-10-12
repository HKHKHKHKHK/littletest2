from typing import List

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from littletest.items import zhiPinItem
from scrapy_redis.spiders import RedisSpider
from scrapy import Spider

class ZhipinSpider(Spider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/']
    #redis_key = 'zhipin:start_urls'
    def parse(self, response):
        pages = response.xpath("//div[@class='job-menu']//li//div[@class='text']//a//@href").extract()
        #item['job_names'] = response.xpath("//div[@class='job-menu']//li//div[@class='text']//a//text()").extract()
        for page in pages:
            link = 'https://www.zhipin.com' + page
            yield scrapy.Request(url=link,callback=self.parse_item)


    def parse_item(self, response):
        item = zhiPinItem()
        item['job_links'] = response.url
        print(response.url)
        yield item
