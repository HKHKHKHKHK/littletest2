# -*- coding: utf-8 -*-
import scrapy


class Test2Spider(scrapy.Spider):
    name = 'test2'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']

    def parse(self, response):
        pass
