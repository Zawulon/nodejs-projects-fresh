# -*- coding: utf-8 -*-

# Scrapy settings for pitax project
import datetime
report_datetime = datetime.datetime.now()
dateTimeString = report_datetime.strftime("%Y%m%d_%H-%M-%S")
report_datetime_sql = report_datetime.strftime("%Y-%m-%d %H:%M:%S")
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pitax'

SPIDER_MODULES = ['pitax.spiders']
NEWSPIDER_MODULE = 'pitax.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PitaxCrawler (+https://www.pitax.pl)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
 #   'pitax.middlewares.PitaxSpiderMiddleware': 543,
#    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'pitax.middlewares.PitaxDownloaderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'pitax.pipelines.PitaxPipeline': 300,
#}

ITEM_PIPELINES = {
    'pitax.pipelines.Sqlite3Pipeline': 300,
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 20
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 3600
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Logging and stats
DEPTH_STATS_VERBOSE = True
LOG_FILE = "crawled_history/PitaxCrawler_%s.txt" % dateTimeString

#Store pages folder
LOG_FOLDER = "crawled_history/%s" % dateTimeString

SQLITE_FILE = 'sqlite.db'
SQLITE_TABLE = 'PitaxCrawlResult'

SPLASH_URL = 'http://localhost:8050'
# Feed export
#FEED_FORMAT = 'csv'
#FEED_EXPORT_FIELDS = ['parse_time', 'status', 'title', 'url', 'headers']
#FEED_URI = "export/PitaxCrawler_%s.csv" % dateTimeString