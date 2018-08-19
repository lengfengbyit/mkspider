# -*- coding: utf-8 -*-
# 农历数据爬虫
import scrapy, time, json
from mkspider.lib.models import Lunar
from mkspider.lib.db import session
from mkspider.lib.common import slog, date_operate
from mkspider.items import Lunar as LunarItem


class LunarSpider(scrapy.Spider):
    name = 'lunar'
    allowed_domains = ['www.sojson.com']
    start_urls = [
        'https://www.sojson.com/open/api/lunar/json.shtml?date=%s']

    # 开始抓取数据的日期
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # 爬虫结束日期
    end_date = '2025-12-31'

    custom_settings = {'DOWNLOAD_DELAY': 8}

    def start_requests(self):
        # 获得数据库中得最后日期
        lastLunar = session.query(Lunar).order_by(Lunar.year.desc()).order_by(Lunar.month.desc()).order_by(Lunar.day.desc()).first()

        if lastLunar:
            last_date = "-".join([str(lastLunar.year), str(lastLunar.month), str(lastLunar.day)])
            self.date = date_operate(last_date, 1)

        return [scrapy.Request(self.next_url())]

    def parse(self, response):

        json_data = json.loads(response.body)

        if not json_data or json_data['status'] != 200:
            slog('D', '[%s]数据爬取失败....' % self.date)
            print(json_data)
            exit(0)
        else:
            lunarItem = LunarItem(**json_data['data'])
            yield lunarItem

        self.date = date_operate(self.date, 1)
        if self.date <= self.end_date:
            yield scrapy.Request(self.next_url())

    def next_url(self):
        """ 返回下一个url链接 """
        return self.start_urls[0] % self.date
