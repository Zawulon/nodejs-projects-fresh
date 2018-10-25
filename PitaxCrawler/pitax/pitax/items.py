# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PitaxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parse_time = scrapy.Field()
    status = scrapy.Field()
    varnish_status = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    headers = scrapy.Field()
    
    counter = scrapy.Field()
    crawl_date = scrapy.Field()
    crawl_found = scrapy.Field()
    crawl_url = scrapy.Field()
    link_text = scrapy.Field()     
    
    pass
