import csv
import sqlite3


sqlite_file = 'pitax\pitax\spiders\sqlite.db'


report_sql = """select pcl.[crawl_date]
    ,lc.[Account]
    ,pcl.[crawl_url]
	,pcl.[crawl_status]
	,pcl.[crawl_found]
	,pcl.[crawl_title]
	--,pcl.[link_text]
from PitaxCrawlResult pcl
LEFT OUTER JOIN LinksToCrawl lc ON (lc.UrlToCrawl == pcl.[crawl_url] AND lc.[UseForCrawl] = 'yes')
where date(pcl.crawl_date) == (select date(max(crawl_date)) from PitaxCrawlResult)

order by lc.UrlToCrawl"""

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

with open('Export.csv', 'x', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    cur.execute(report_sql)
    rows = cur.fetchall()
    writer.writerows(rows)
       
    conn.commit()
    conn.close()