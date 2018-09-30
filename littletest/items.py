# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class liePinItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    nextPage = scrapy.Field()
    salary = scrapy.Field()

class zhiPinItem(scrapy.Item):
    # define the fields for your item here like:
    job_names = scrapy.Field()
    job_links = scrapy.Field()

