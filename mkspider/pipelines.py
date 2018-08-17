# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lib.db import session
from lib.models import *
from lib.common import get_weekth_by_date

class MkspiderPipeline(object):

    def open_spider(self, spider):
        self.spider_items = {
            'ana':  self.ana_item,
            'constellation_day': self.constellation_day_item,
            'astro': self.astro_item
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
            item['year']['name'] = item['astroname']
            item['year']['astroid'] = item['astroid']

            astroYear = AstroYear(**item['year'])
            session.add(astroYear)
            session.commit()
        if item['month']:
            item['month']['name'] = item['astroname']
            item['month']['astroid'] = item['astroid']
            year, month = item['month']['date'].split('-')
            item['month']['date'] = "{}{}".format(year, str(month).zfill(2))

            astroMonth = AstroMonth(**item['month'])
            session.add(astroMonth)
            session.commit()
        if item['week']:
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
            item['today']['name'] = item['astroname']
            item['today']['astroid'] = item['astroid']

            astroDay = AstroDay(**item['today'])
            session.add(astroDay)
            session.commit()


    def constellation_day_item(self, item):
        """ 星座运势 日数据 存储 """
        constellationDay = ConstellationDay(**item)
        session.add(constellationDay)
        session.commit()

