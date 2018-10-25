# -*- coding: utf-8 -*-
import scrapy
import datetime
import os
import shutil
import time

from scrapy_splash import SplashRequest

    
class PageCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_date = scrapy.Field()
    crawl_url = scrapy.Field()
    crawl_status = scrapy.Field()
    crawl_found = scrapy.Field()
    link_text = scrapy.Field()     
    headers = scrapy.Field()
    parse_time = scrapy.Field()
 #   varnish_status = scrapy.Field()
    crawl_title = scrapy.Field()
    pass


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-test2"
    counter = 0
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    download_delay = 5.0
    handle_httpstatus_list = [502,504,404,301,200]
    report_datetime = datetime.datetime.now()
    dateTimeString = report_datetime.strftime("%Y%m%d_%H-%M-%S")
    report_datetime_sql = report_datetime.strftime("%Y-%m-%d %H:%M:%S")
    with open("url.txt", "rt") as f:
         start_urls = [url.strip() for url in f.readlines()]

 #   def start_requests(self):
 #       for u in self.start_urls:
 #           yield scrapy.Request(u, callback=self.parse_httpbin,
 #                                   errback=self.errback_httpbin,
 #                                   dont_filter=True)
    def start_requests(self):
        for url in self.start_urls:
            time.sleep (3)
            yield SplashRequest(url, self.parse, args={'timeout': 90, 'resource_timeout':20})

    def closed(self, reason):
        print (self.crawler.stats.get_stats())
        zipfilename = self.dateTimeString + '/' + str(self.counter) + 'index.html'
        self.logger.info('Parse output_filename %s', self.dateTimeString)
        output_filename = os.path.dirname(zipfilename) + ".zip"
        self.logger.info('Parse outpuoutput_filename %s', output_filename)
        if os.path.exists(os.path.dirname(zipfilename)):
            shutil.make_archive(output_filename, 'zip', os.path.dirname(zipfilename))
            shutil.rmtree(os.path.dirname(zipfilename), ignore_errors=True)
            ff = output_filename+'.zip'
            dst_file = os.path.join('crawled_history', ff)
            shutil.move(ff, dst_file)

    def parse(self, response):
        self.counter+=1
        item = PageCrawlerItem()
        item['crawl_status'] = response.status
        item['crawl_url'] = response.url
        item['link_text'] = ''
        item['crawl_found'] = 0
        item['crawl_date'] =self.report_datetime_sql
        item['parse_time'] = ''
        item['crawl_title'] = ''
        item['headers'] = ''
        if  200 <= response.status <= 505:
            filename = self.dateTimeString + '/' + str(self.counter) + 'index.html'
            if not os.path.exists(os.path.dirname(filename)):
               os.makedirs(os.path.dirname(filename))
            try:
               html_file = open(filename, 'wb')
               html_file.write(response.body)
               
               html_file.close()
            except:
               print('Error saving file:{}'.format(filename))
            item['parse_time'] = response.headers['Date']
            item['crawl_title'] = response.xpath('//title/text()')[0].extract()
            item['headers'] = response.headers
            
            quoteslist = []
            quotes = response.xpath('(//a[contains(@href, "pitax.pl")])|(//a[contains(@href, "iwop.pl")])')
            for quote in quotes:
                quoteslist.append(quote.extract()) 
             
            if(len(quotes) > 0):
                  item['crawl_found'] = 1
                  item['link_text'] = ','.join(quoteslist)
        yield item
        
