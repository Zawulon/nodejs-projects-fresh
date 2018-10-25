# -*- coding: utf-8 -*-
import scrapy
import datetime
import os
import shutil
import time
import sqlite3

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
    name = "toscrape-test"
    counter = 0
    linksid = []
    urlslist = []
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    handle_httpstatus_list = [502,504,404,301,200,403]
    report_datetime = datetime.datetime.now()
    dateTimeString = report_datetime.strftime("%Y%m%d_%H-%M-%S")
    report_datetime_sql = report_datetime.strftime("%Y-%m-%d %H:%M:%S")
    start_urls = [
        'http://www.koscian.net/Rozliczanie_pit_online_ze_strata_podatkowa,28744.html',
    ]

    def start_requests(self):      
        selectlinks_sql = "SELECT max([LinkId]),[UrlToCrawl] FROM [LinksToCrawl] where UrlToCrawl like 'http%' group by UrlToCrawl order by UrlToCrawl"
        sqlite_file = self.settings.get('SQLITE_FILE')
        conn = sqlite3.connect(sqlite_file)
        cur = conn.cursor()
        for row in cur.execute(selectlinks_sql):
            self.linksid.append(row[0])
            self.urlslist.append(row[1])
        #    print(row[1])
        conn.close()
        for url in self.urlslist:
            time.sleep (3)
            yield SplashRequest(url, self.parse, args={'timeout': 90, 'resource_timeout':20})
    
    def closed(self, reason):
        print (self.crawler.stats.get_stats())
        zipfilename = self.dateTimeString + '/' + str(self.counter) + 'index.html'
        self.logger.info('Parse output_filename %s', self.dateTimeString)
        output_filename = os.path.dirname(zipfilename)
        self.logger.info('Parse outpuoutput_filename %s', output_filename)
        if os.path.exists(os.path.dirname(zipfilename)):
            shutil.make_archive(output_filename, 'zip', os.path.dirname(zipfilename))
            shutil.rmtree(os.path.dirname(zipfilename), ignore_errors=True)
            ff = output_filename+'.zip'
            dst_file = os.path.join('crawled_history', ff)
            shutil.move(ff, dst_file)

    def parse(self, response):
        time.sleep (5)
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
        if  200 <= response.status <= 500:
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
            