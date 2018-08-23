# -*- coding: utf-8 -*-
""" 星座运势 极速数据api """
import scrapy, time, sys, json
from mkspider.items import Astro
from mkspider.lib.models import AstroYear, AstroMonth, AstroWeek, AstroDay
from mkspider.lib.db import session, engine
from mkspider.lib.common import get_weekth_by_date, date_operate, default_val, date2str
from mkspider.settings import ASTRO_LIST


class AstroSpider(scrapy.Spider):
    name = 'astro'
    allowed_domains = ['api.jisuapi.com']
    start_urls = [
        'http://api.jisuapi.com/astro/fortune?astroid=%s&date=%s&appkey=%s']

    # 聚合数据app key
    # appkeys = [
    #     'c4a1884edcc9cd42',  # lengfengbyit
    #     '400160c5118b2eaa',  # 13458672106
    #     'd1192a8a9cc0ed6d',  # 17089596845
    #     '717f6791d371967a',  # 17156482110
    #     'c4970c4dfc7bdc43',  # 17044764762
    #     'dc821167ab04f1c5',  # 17078048821
    #     '9b1d5862954c2d57',  # 17174738820
    # ]

    appkeys = {
        'c4a1884edcc9cd42': 0,
        '400160c5118b2eaa': 0,
        'd1192a8a9cc0ed6d': 0,
        '717f6791d371967a': 0,
        'c4970c4dfc7bdc43': 0,
        'dc821167ab04f1c5': 0,
        '9b1d5862954c2d57': 0,
    }

    # 默认使用appkey的索引
    appkey_index = 0
    
    # 星座id 按时间顺序 1：白羊座 12：双鱼座
    astroid = 1
    # 获得当前日期
    date = '2016-01-01'
    year = {
        'date': 0,
        'astroid': 0
    }
    weekth = year.copy()
    month = year.copy()

    custom_settings = {'CONCURRENT_REQUESTS': 10}
   
    def start_requests(self):
        
        # 初始化爬取链接
        self.init_start_urls()
   
        # 查询数据库中最后日期的星座数据
        lastDayAstro = session.query(AstroDay).order_by(
            AstroDay.date.desc()).order_by(AstroDay.astroid.desc()).first()
        if lastDayAstro:
            self.date = lastDayAstro.date.strftime("%Y-%m-%d")
            if lastDayAstro.astroid == 12:
                self.date = date_operate(self.date, 1)
            else:
                self.astroid = lastDayAstro.astroid + 1
    
        # 查询最后一条周数据
        """ lastWeekAstro = session.query(AstroWeek).order_by(
            AstroWeek.weekth.desc()).order_by(AstroWeek.astroid.desc()).first()
        if lastWeekAstro:
            self.weekth['date'] = lastWeekAstro.weekth
            self.weekth['astroid'] = lastWeekAstro.astroid """

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
        
        self.astroid -= 1
        start_url = self.next_url()
        if start_url:
            return [scrapy.Request(start_url)]
        else:
            self.logger.error('不存在可用的appkey')
            return []

    def parse(self, response):
      
        json_data = json.loads(response.body)
        star = ASTRO_LIST[self.astroid - 1]
        # 标志是否爬取结束
        is_end = False
        
        if json_data['status'] != "0":

            msg = default_val(json_data, 'msg', '数据爬取失败, 重新爬取...')
            log = "[{}][{}]{}".format(star, self.date, msg)
            self.logger.error(log)

            old_appkey = response.url[-16:]
            self.appkeys[old_appkey] = 100

            # 爬取失败，更换appkey继续爬取
            appkey = self.get_appkey()
            if appkey:

                # 当前url更换appkey
                url = '%s%s' % (response.url[:-16], appkey) 
                self.logger.info('更换appkey继续爬取,appkey为:%s' % appkey)

                # 设置该请求的优先级为100, 一般该参数的默认值为0，
                # 数值越大，越先执行
                yield scrapy.Request(url, priority=100)
            else:       
                is_end = True
        else:
            self.logger.info("[%s][%s]数据爬取成功...." % (star, self.date))
            astro = Astro(**json_data['result'])
            yield astro

        if not is_end:
            # 获得下一个请求链接
            yield scrapy.Request(self.next_url())
        

    def next_url(self):
        """ 获得下一个url """
        self.astroid += 1
        if self.astroid > 12:
            self.astroid = 1
            self.date = date_operate(self.date, 1)
        
        appkey = self.get_appkey()
        if not appkey:
            return False
        # appkey = self.appkeys[self.appkey_index]
        url = self.start_urls[0] % (self.astroid, self.date, appkey)
        self.logger.debug("爬取URL:%s" % url)
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

    def get_appkey(self):
        """ 获得appkey """
        for appkey,count in self.appkeys.items():
            if count < 100:
                self.appkeys[appkey] += 1
                return appkey
                break

        return False

    def init_start_urls(self):
        """ 获得遗漏的星座和日期，添加到start_urls中 """
        sql = """
            SELECT `date`, COUNT(*) c FROM astro_day
            GROUP BY `date`
            HAVING c < 12
            ORDER BY c DESC
        """
        # 所有的星座id
        astroids = set(range(1, 13))
        result = engine.execute(sql).fetchall()
        for date,count  in result:
            date = date.strftime('%Y-%m-%d')
            # 获得该日期下的所有星座id
            res = session.query(AstroDay.astroid).filter_by(date=date).all()
            astroids_date = set(map(lambda x: x[0], res))
            # 求差集, 得到遗漏的星座id
            astroids_diff = list(astroids - astroids_date)
            # 同个星座id和日期构造请求链接
            for astroid in astroids_diff:
                self.astroid = astroid - 1
                self.date = date
                url = self.next_url()
                self.start_urls.append(url)
