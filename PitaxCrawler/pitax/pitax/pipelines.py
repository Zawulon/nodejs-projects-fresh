# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class QuotesbotPipeline(object):
#    def process_item(self, item, spider):
#        return item
        

import sqlite3


class Sqlite3Pipeline(object):

    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'), # 从 settings.py 提取
            sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        #insert_sql = "insert into {0}({1}) values ({2})".format(self.sqlite_table, 
        #                                                        ', '.join(item.fields.keys()),
        #                                                        ', '.join(['?'] * len(item.fields.keys())))
        #print(insert_sql)
        insert_sql = "INSERT INTO [PitaxCrawlResult] ([crawl_date],[crawl_url],[crawl_status],[crawl_found],[link_text],[parse_time],[crawl_title]) VALUES (?,?,?,?,?,?,?)"

        list = []
        colkeys = ['crawl_date','crawl_url','crawl_status','crawl_found','link_text','parse_time','crawl_title']
        for ck in colkeys:
            list.append(item[ck])
        

       # for key in item.fields.keys():
       #     list.append(str(item[key])) 
        self.cur.execute(insert_sql, list)
        self.conn.commit()
        
        return item