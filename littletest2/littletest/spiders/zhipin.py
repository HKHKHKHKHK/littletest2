from typing import List

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from littletest.items import zhiPinItem

class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/']

    def parse(self, response):
        pages = response.xpath("//div[@class='job-menu']//li//div[@class='text']//a//@href").extract()
        #item['job_names'] = response.xpath("//div[@class='job-menu']//li//div[@class='text']//a//text()").extract()
        for page in pages:
            link = 'https://www.zhipin.com' + page
            yield scrapy.Request(url=link,callback=self.parse_item,dont_filter=True,meta={'download_timeout':10})


    def parse_item(self, response):
        item = zhiPinItem()
        item['job_links'] = response.url
        print(response.url)
        yield item
