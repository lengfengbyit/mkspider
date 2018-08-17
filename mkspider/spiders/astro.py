# -*- coding: utf-8 -*-
""" 星座运势 极速数据api """
import scrapy, time, sys, json
from mkspider.items import Astro
from mkspider.lib.models import AstroYear, AstroMonth, AstroWeek, AstroDay
from mkspider.lib.db import session
from mkspider.lib.common import slog, get_weekth_by_date, date_operate
from mkspider.settings import ASTRO_LIST


class AstroSpider(scrapy.Spider):
    name = 'astro'
    allowed_domains = ['api.jisuapi.com']
    start_urls = [
        'http://api.jisuapi.com/astro/fortune?astroid=%s&date=%s&appkey=c4a1884edcc9cd42']

    # 爬取失败的url
    error_urls = []
    
    # 星座id 按时间顺序 1：白羊座 12：双鱼座
    astroid = 1
    # 获得当前日期
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    year = {
        'date': 0,
        'astroid': 0
    }
    weekth = year.copy()
    month = year.copy()

   
    def start_requests(self):
        # 查询数据库中最后日期的星座数据
        lastDayAstro = session.query(AstroDay).order_by(
            AstroDay.date.desc()).order_by(AstroDay.astroid.desc()).first()
        if lastDayAstro:
            if lastDayAstro.astroid == 12:
                self.date = date_operate(lastDayAstro.date, 1)
            else:
                self.date = lastDayAstro.date.strftime("%Y-%m-%d")
                self.astroid = lastDayAstro.astroid + 1
    
        # 查询最后一条周数据
        lastWeekAstro = session.query(AstroWeek).order_by(
            AstroWeek.weekth.desc()).order_by(AstroWeek.astroid.desc()).first()
        if lastWeekAstro:
            self.weekth['date'] = lastWeekAstro.weekth
            self.weekth['astroid'] = lastWeekAstro.astroid

        #查询最后一条月数据
        lastMonthAstro = session.query(AstroMonth).order_by(
            AstroMonth.date.desc()).order_by(AstroMonth.astroid.desc()).first()
        if lastMonthAstro:
            self.month['date'] = lastMonthAstro.date
            self.month['astroid'] = lastMonthAstro.astroid
      
        # 查询最后一条年数据
        lastYearAstro = session.query(AstroYear).order_by(AstroYear.date.desc()).order_by(AstroYear.astroid.desc()).first()
        if lastYearAstro:
            self.year['date'] = lastYearAstro.date
            self.year['astroid'] = lastYearAstro.astroid
        start_url = self.start_urls[0] % (self.astroid, self.date)
        slog('D', "初始化URL:%s" % start_url)
        return [scrapy.Request(start_url)]
        

    def parse(self, response):
        
        json_data = json.loads(response.body)
        star = ASTRO_LIST[self.astroid - 1]

        if json_data['status'] != "0":
            slog('E', "[%s][%s]数据爬取失败, 重新爬取..." % (star, self.date))
            self.error_urls.append(response.url)
            sys.exit(0)
            yield scrapy.Request(self.next_url())
        else:
            slog('I', "[%s][%s]数据爬取成功...." % (star, self.date))
            astro = Astro(**json_data['result'])
            astro = self.data_check(astro)
            print(astro)
            yield astro

        # 获得下一个请求链接
        # yield scrapy.Request(self.next_url())
        

    def next_url(self):
        """ 获得下一个url """
        self.astroid += 1
        if self.astroid > 12:
            self.astroid = 1
            self.date = date_operate(self.date, 1)
        
        url = self.start_urls[0] % (self.astroid, self.date)
        slog('D', "爬取URL:%s" % url)
        return url

    def data_check(self, astro):
        """ 数据检查 """
        # 获得爬取日期对应的年月日,周数
        # 如果数据库中存在，则不更新
        # 否则，则更新，并记录最新数据的年月日和周数
        year, month, day = self.date.split('-')
        weekth = get_weekth_by_date(self.date)
        month = int("{}{}".format(year, month))
        if self.year['date'] >= year and self.astroid <= self.year['astroid']:
            astro['year'] = False
        else:
            self.year['date'] = year
            self.year['astroid'] = self.astroid

        if self.month['date'] >= month and self.astroid <= self.month['astroid']:
            astro['month'] = False
        else:
            self.month['date'] = month
            self.month['astroid'] = self.astroid
     
        if self.weekth['date'] >= weekth and self.astroid <= self.weekth['astroid']:
            astro['week'] = False
        else:
            self.weekth['date'] = weekth
            self.weekth['astroid'] = self.astroid

        return astro
