# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ana(scrapy.Item):
    """ 名言警句 """
    
    title = scrapy.Field()
    author = scrapy.Field()
    froms = scrapy.Field() 
    tags = scrapy.Field() 
    like_count = scrapy.Field() 
    dislike_count = scrapy.Field()


class ConstellationDay(scrapy.Item):
    """ 星座运势 日数据 """
    name = scrapy.Field()
    all = scrapy.Field()
    color = scrapy.Field()
    health = scrapy.Field()
    love = scrapy.Field()
    money = scrapy.Field()
    number = scrapy.Field()
    qfriend = scrapy.Field()
    summary = scrapy.Field()
    work = scrapy.Field()
    date = scrapy.Field()


class Astro(scrapy.Item):
    """ 星座运势 """
    astroid = scrapy.Field()
    astroname = scrapy.Field()
    year = scrapy.Field()
    week = scrapy.Field()
    today = scrapy.Field()
    month = scrapy.Field()
    tomorrow = scrapy.Field()

class AstroDay(scrapy.Item):
    """ 星座运势 日数据 """
    name = scrapy.Field()
    presummary = scrapy.Field()
    color = scrapy.Field()
    health = scrapy.Field()
    love = scrapy.Field()
    money = scrapy.Field()
    number = scrapy.Field()
    summary = scrapy.Field()
    career = scrapy.Field()
    date = scrapy.Field()

class AstroWeek(scrapy.Item):
    """ 星座运势 周数据 """
    name = scrapy.Field()
    weekth = scrapy.Field()
    health = scrapy.Field()
    job = scrapy.Field()
    love = scrapy.Field()
    money = scrapy.Field()
    career = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()

class AstroMonth(scrapy.Item):
    """ 星座运势 月数据 """
    name = scrapy.Field()
    summary = scrapy.Field()
    health = scrapy.Field()
    love = scrapy.Field()
    money = scrapy.Field()
    career = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()

class AstroYear(scrapy.Item):
    """ 星座运势 年数据 """
    name = scrapy.Field()
    summary = scrapy.Field()
    career = scrapy.Field()
    lovel = scrapy.Field()
    money = scrapy.Field()
    date = scrapy.Field()
