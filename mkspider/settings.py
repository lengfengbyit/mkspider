# -*- coding: utf-8 -*-

# Scrapy settings for mkspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import sys
try:
    reload(sys)
    # 设置默认编码为utf-8
    sys.setdefaultencoding('utf-8')
except Exception:
    pass


BOT_NAME = 'mkspider'

SPIDER_MODULES = ['mkspider.spiders']
NEWSPIDER_MODULE = 'mkspider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mkspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mkspider.middlewares.MkspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'mkspider.middlewares.MkspiderDownloaderMiddleware': 543,
    # 'mkspider.middlewares.IPProxy': 543,
    'mkspider.middlewares.RandomUserAgent': 544,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'mkspider.pipelines.MkspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 数据库配置
DB_CONFIG = "mysql+pymysql://toolbar:Toolbar_System+123@127.0.0.1:3306/maiku_api?charset=utf8"

# 日志配置
LOG_ENABLED = True
LOG_ENCODING = "UTF-8"
LOG_LEVEL = "DEBUG"

# 12星座
ASTRO_LIST = [
    "白羊座",
    "金牛座",
    "双子座",
    "巨蟹座",
    "狮子座",
    "处女座",
    "天秤座",
    "天蝎座",
    "射手座",
    "摩羯座",
    "水瓶座",
    "双鱼座"
]


# 省会名称，只支持这些省会的天气查询
PROVINCES = [
    '北京',
    '天津',
    '上海',
    '重庆',
    '石家庄',
    '郑州',
    '武汉',
    '长沙',
    '南京',
    '南昌',
    '沈阳',
    '长春',
    '哈尔滨',
    '西安',
    '太原',
    '济南',
    '成都',
    '西宁',
    '合肥',
    '海口',
    '广州',
    '贵阳',
    '杭州',
    '福州',
    '台北',
    '兰州',
    '昆明',
    '拉萨',
    '银川',
    '南宁',
    '乌鲁木齐',
    '呼和浩特',
    '香港',
    '澳门'
]
