# -*- coding: utf-8 -*-
import scrapy


class CqcSpider(scrapy.Spider):
    name = 'cqc'
    allowed_domains = ['cuiqingcai.com']
    start_urls = ['http://cuiqingcai.com/']

    def parse(self, response):
        pass
