# -*- coding: utf-8 -*-
# 和风天气数据api爬虫
import scrapy, json
from mkspider.lib.db import session
from mkspider.lib.models import Weather
from mkspider.items import Weather as WeatherItem
from mkspider.lib.common import slog, date_operate, default_val, weather_data_check
from mkspider.settings import PROVINCES

class WeatherHefengSpider(scrapy.Spider):
    name = 'weather_hefeng'
    allowed_domains = ['free-api.heweather.com']
    start_urls = [
        'https://free-api.heweather.com/s6/weather?key=7afbc9166b37449ab42312177e47610a&location=%s']
        

    provinces = PROVINCES

    # 天气类型对应提醒
    types = {}

    # 当前要爬取的省会城市下标
    index = 0

    # 爬虫配置，下载延迟5秒
    # custom_settings = {'DOWNLOAD_DELAY': 5}
    
    def start_requests(self):
        self.index = weather_data_check(self.provinces)
        if self.index >= len(self.provinces):
            slog("D", "今日天气数据已爬取完毕")
            return []
    
        # 初始化天气类型数据
        self.init_types()
        return [scrapy.Request(self.next_url())]

    def parse(self, response):
        json_data = json.loads(response.body)
        json_data = json_data['HeWeather6'][0]
        city = self.provinces[self.index]
        if not json_data or json_data['status'] != 'ok':
            slog('E', '[%s]天气信息爬取失败' % city)
            exit(0)

        slog("D", "[%s]天气信息爬取成功" % city)

        # 未来5天的列表数据
        forecast = []
        base_data = {}
        i = 0
        for item in json_data['daily_forecast']:
            if i == 0:
                base_data['date'] = item['date'].replace('-', '')
                base_data['shidu'] = '{}%'.format(item['hum'])
                base_data['pm25'] = ''
                base_data['pm10'] = ''
                base_data['quality'] = ''
                # 获得最高温度和最低温度的中间值
                high = int(item['tmp_max'])
                low = int(item['tmp_min'])
                base_data['wendu'] = high - round((high - low) / 2)
            
            tmp = {
                'sunrise': item['sr'],
                'sunset': item['ss'],
                'high': item['tmp_max'],
                'low':item['tmp_min'],
                'aqi': '',
                'fx': item['wind_dir'],
                'fl': '<{}级'.format(item['wind_sc'].split('-')[1]),
                'type': item['cond_txt_d'],
                'notice': default_val(self.types, item['cond_txt_d'], json_data['lifestyle'][0]['txt']),
            }
            
            forecast.append(tmp)
            i += 1

        base_data['city'] = json_data['basic']['location']
        base_data['forecast'] = forecast
     
        weather_item = WeatherItem(**base_data)

        yield weather_item

        self.index += 1
        if self.index < len(self.provinces):
            yield scrapy.Request(self.next_url())

    def next_url(self):
        return self.start_urls[0] % self.provinces[self.index]


    def init_types(self):
        """ 初始化天气类型数据 """
        types = session.query(
            Weather.stype, Weather.notice).group_by('stype').all()
        for item in types:
            self.types[item[0]] = item[1]
