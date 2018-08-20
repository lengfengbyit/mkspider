# -*- coding: utf-8 -*-
# 天气爬虫
import scrapy, json, time
from mkspider.lib.db import session
from mkspider.lib.models import Weather
from mkspider.items import Weather as WeatherItem
from mkspider.lib.common import slog, date_operate, default_val


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['www.sojson.com']
    start_urls = ['https://www.sojson.com/open/api/weather/json.shtml?city=%s']

    # 省会名称，只支持这些省会的天气查询
    provinces = [
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

    # 当前要爬取的省会城市下标
    index = 0

    # 爬虫配置，下载延迟5秒
    custom_settings = {'DOWNLOAD_DELAY': 5}

    def start_requests(self):
        curr_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 查询当前日期最后一个城市名称
        date_weather = session.query(Weather).filter_by(date=curr_date).order_by(Weather.id.desc()).first()
        city = str(date_weather.city.decode('utf-8'))
        if date_weather:
            # 判断当前日期是否查询
            city_last_weather = session.query(Weather).filter_by(city=city).order_by(Weather.date.desc()).first()
            if city_last_weather and city_last_weather.date != date_operate(curr_date, 4):
                self.index = self.provinces.index(city) + 1
        if self.index >= len(self.provinces):
            slog("D", "今日天气数据已爬取完毕")
            exit(0)
        return [scrapy.Request(self.next_url())]

    def parse(self, response):
        
        json_data = json.loads(response.body)
        city = self.provinces[self.index]
        if not json_data or json_data['status'] != 200:
            slog('E', '[%s]天气信息爬取失败' % city)
            exit(0)
        
        slog("D", "[%s]天气信息爬取成功" % city)
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
