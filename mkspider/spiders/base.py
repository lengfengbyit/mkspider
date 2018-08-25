# -*- coding: utf-8 -*-
# 爬虫基类，提供一些公共操作
import scrapy, pprint
from mkspider.lib.common import send_email


class BaseSpider(scrapy.Spider):

    def parse(self, response):
        pass

    def closed(self, reason):
        """ 爬虫结束时发送邮件 """
        reason = pprint.pformat(self.crawler.stats.get_stats())
        send_email('spider name: %s' % self.name, reason, self.logger)