# -*- coding: utf-8 -*-
""" 星座运势 日数据 爬取 """
import scrapy, logging, json, time
from mkspider.settings import ASTRO_LIST
from mkspider.items import ConstellationDay

class ConstellationDaySpider(scrapy.Spider):
    name = 'constellation_day'
    allowed_domains = ['web.juhe.cn']
    start_urls = [
        'http://web.juhe.cn:8080/constellation/getAll?consName=%s&type=today&key=4714ef4a87cfa9979352e72790d8e70b']
    index = 0

    def start_requests(self):
        start_url = self.start_urls[0] % ASTRO_LIST[self.index]
        return [scrapy.Request(start_url)]

    def parse(self, response):
        
        self.logger.info("-----------[%s]数据爬取" % ASTRO_LIST[self.index])
       
        json_data = json.loads(response.body)
        if json_data['error_code'] != 0:
            self.logger.error('数据爬取出错')
            return

        try:
            date = json_data['date']
            qfriend = json_data['QFriend']
            del json_data['date']
            del json_data['QFriend']
            del json_data['error_code']
            del json_data['datetime']
            del json_data['resultcode']
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(json_data)
            return

        date = time.strftime(
            "%Y-%m-%d", time.strptime(str(date), "%Y%m%d"))

        constellationDay = ConstellationDay(**json_data)
        constellationDay['date'] = date
        constellationDay['qfriend'] = qfriend
        yield constellationDay

        self.index += 1
        if self.index < len(ASTRO_LIST):
            next_link = self.start_urls[0] % ASTRO_LIST[self.index]
            yield scrapy.Request(next_link)
