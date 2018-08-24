# -*- coding: utf-8 -*-
# 天气爬虫
import scrapy, json, urllib
from mkspider.items import Weather as WeatherItem
from mkspider.lib.common import date_operate, default_val, weather_data_check, send_email
from mkspider.settings  import PROVINCES


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['www.sojson.com']
    start_urls = ['https://www.sojson.com/open/api/weather/json.shtml?city=%s']

    provinces = PROVINCES

    # 当前要爬取的省会城市下标
    index = 0

    # 爬虫配置，下载延迟5秒
    custom_settings = {'DOWNLOAD_DELAY': 5}

    # 记录请求次数
    request_count = 0

    def start_requests(self):
        self.index = weather_data_check(self.provinces)
        if self.index >= len(self.provinces):
            self.logger.info("今日天气数据已爬取完毕")
            return []
        return [scrapy.Request(self.next_url())]

    def parse(self, response):
        scrapy.shell.inspect_response(response, self)
        # 一共34个城市，最多请求50次
        self.request_count += 1
        if self.request_count >= 50:
            return

        json_data = json.loads(response.body)
        city = response.url.split('city=')[1]
        # url 解码
        city = urllib.unquote(city)
        if not json_data or json_data['status'] != 200:
            self.logger.error('[%s]天气信息爬取失败,重新爬取' % city)
            
            # 重新爬取，设置高优先级，并且不重复过滤机制过滤
            yield scrapy.Request(response.url, priority=100, dont_filter=True)
        else:
        
            self.logger.info("[%s]天气信息爬取成功" % city)

            weather_item = WeatherItem(
                city = json_data['city'],
                date = json_data['date'],
                shidu = json_data['data']['shidu'],
                pm25 = default_val(json_data['data'], 'pm25'),
                pm10 = default_val(json_data['data'], 'pm10'),
                quality = default_val(json_data['data'], 'quality'),
                wendu = json_data['data']['wendu'],
                forecast = json_data['data']['forecast']
            )

            yield weather_item
        
        self.index += 1
        if self.index < len(self.provinces):
            yield scrapy.Request(self.next_url())

    def next_url(self):
        return self.start_urls[0] % self.provinces[self.index]

    def closed(self, reason):
        """ 爬虫结束时发送邮件 """
        send_email('spider name: %s' % self.name, reason, self.logger)
