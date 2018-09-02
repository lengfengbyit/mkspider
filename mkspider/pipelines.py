# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,re
from mkspider.lib.db import session
from mkspider.lib.models import *
from mkspider.lib.common import get_weekth_by_date, date_operate
# from xpinyin import Pinyin

class MkspiderPipeline(object):

    def open_spider(self, spider):
        self.spider_items = {
            'ana':  self.ana_item,
            'constellation_day': self.constellation_day_item,
            'astro': self.astro_item,
            'lunar': self.lunar_item,
            'star': self.star_item,
            'weather': self.weather_item,
            'weather_hefeng': self.weather_item,
        }

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):

        if spider.name in self.spider_items:
            return self.spider_items[spider.name](item)

    def ana_item(self, item):
        """ 名言警句数据存储 """
        ana = Ana(**item)
        session.add(ana)
        session.commit()

    def astro_item(self, item):
        """ 星座运势 数据存储 """
        if item['year']:
            res = session.query(AstroYear).filter_by(
                astroid=item['astroid']).filter_by(date=item['year']['date']).first()

            if not res:
                item['year']['name'] = item['astroname']
                item['year']['astroid'] = item['astroid']

                astroYear = AstroYear(**item['year'])
                session.add(astroYear)
                session.commit()

        if item['month']:

            year, month = item['month']['date'].split('-')
            item['month']['date'] = "{}{}".format(year, str(month).zfill(2))

            res = session.query(AstroMonth).filter_by(
                astroid=item['astroid']).filter_by(date=item['month']['date']).first()
            if not res:
                item['month']['name'] = item['astroname']
                item['month']['astroid'] = item['astroid']

                astroMonth = AstroMonth(**item['month'])
                session.add(astroMonth)
                session.commit()


        if item['week'] and False:

            item['week']['name'] = item['astroname']
            item['week']['astroid'] = item['astroid']
            item['week']['weekth'] = get_weekth_by_date(item['today']['date'])
            start_date, end_date = item['week']['date'].split('~')
            end_date = "{}-{}".format(start_date.split('-')[0], end_date)
            item['week']['start_date'] = start_date
            item['week']['end_date'] = end_date
            del item['week']['date']

            astroWeek = AstroWeek(**item['week'])
            session.add(astroWeek)
            session.commit()

        if item['today']:

            res = session.query(AstroDay).filter_by(
                astroid=item['astroid']).filter_by(date=item['today']['date']).first()

            item['today']['name'] = item['astroname']
            item['today']['astroid'] = item['astroid']

            try:
                # 判断number属性是否是数字类型
                if not str(item['today']['number']).isdigit():
                    item['today']['number'] = 0
                astroDay = AstroDay(**item['today'])
                session.add(astroDay)
                session.commit()
            except Exception:
                pass


    def lunar_item(self, item):
        """ 农历数据存储 """

        item['festivalList'] = ",".join(item['festivalList'])
        item['jieqi'] = json.dumps(item['jieqi'])

        lunar = Lunar(**item)
        session.add(lunar)
        session.commit()

    def star_item(self, item):
        """ 明星数据存储 """

        p = Pinyin()
        item['name_initial'] = p.get_initials(item['name'], '')
        item['name_spell'] = p.get_pinyin(item['name'], '')

        star = Star(**item)
        session.add(star)
        session.commit()

    def weather_item(self, item):
        """ 天气数据存储 """
        item['date'] = str(item['date'])
        date = '-'.join([item['date'][0:4], item['date'][4:6], item['date'][6:8]])
        i = 0
        for tmp in item['forecast']:
            curr_date = date_operate(date, i)
            i += 1
            info = {
                'city': item['city'],
                'date': curr_date,
                'shidu': item['shidu'],
                'pm25': item['pm25'],
                'pm10': item['pm10'],
                'quality': item['quality'],
                'wendu': item['wendu'],
                'sunrise': tmp['sunrise'],
                'sunset': tmp['sunset'],
                'high': re.sub('[^\.|\d]', '', tmp['high']), # 只保留数字部分
                'low': re.sub('[^\.|\d]', '', tmp['low']),
                'aqi': tmp['aqi'],
                'fx': tmp['fx'],
                'fl': tmp['fl'],
                'stype': tmp['type'],
                'notice': tmp['notice']
            }
            if not info['pm25']:
                del info['pm25']
                del info['pm10']
                del info['aqi']
                del info['quality']
            weather = Weather(**info)

            # 先判断天气数据是否存在，如果存在则更新
            # 如果不存在则新增
            old_weather = session.query(Weather).filter_by(city=item['city']).filter_by(date=curr_date).first()
            if old_weather:
                session.query(Weather).filter_by(id=old_weather.id).update(info)
            else:
                session.add(weather)
            session.commit()

    def constellation_day_item(self, item):
        """ 星座运势 日数据 存储 """
        constellationDay = ConstellationDay(**item)
        session.add(constellationDay)
        session.commit()
