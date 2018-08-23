# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, CHAR, Date, SMALLINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Histoday(Base):
    __tablename__ = 'histoday'
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    year = Column(SMALLINT, default="2018")
    month = Column(CHAR(2))
    day = Column(CHAR(2))
    date = Column(Date)
    tags = Column(String(100))


class Ana(Base):
    __tablename__ = 'ana'
    id = Column(Integer, primary_key = True)
    title = Column(String(100))
    author = Column(String(30))
    froms = Column(String(30))
    tags = Column(String(50))
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)


class ConstellationDay(Base):
    """ 星座运势 日数据 """
    __tablename__ = 'constellation_day'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    all = Column(String(10))
    color = Column(String(20))
    health = Column(String(10))
    love = Column(String(10))
    money = Column(String(10))
    number = Column(SMALLINT)
    qfriend = Column(String(20))
    summary = Column(String(200))
    work = Column(String(10))
    date = Column(Date)


class AstroDay(Base):
    """ 星座运势 日数据 """
    __tablename__ = 'astro_day'
    id = Column(Integer, primary_key=True)
    astroid = Column(SMALLINT)
    name = Column(String(20))
    presummary = Column(String(500))
    color = Column(String(20))
    health = Column(SMALLINT)
    love = Column(SMALLINT)
    money = Column(SMALLINT)
    number = Column(SMALLINT)
    summary = Column(SMALLINT)
    career = Column(SMALLINT)
    star = Column(String(20))
    date = Column(Date)

class AstroWeek(Base):
    """ 星座运势 周数据 """
    __tablename__ = 'astro_week'
    id = Column(Integer, primary_key=True)
    astroid = Column(SMALLINT)
    name = Column(String(20))
    weekth = Column(SMALLINT)
    health = Column(String(500))
    job = Column(String(500))
    love = Column(String(500))
    money = Column(String(500))
    career = Column(String(500))
    start_date = Column(Date)
    end_date = Column(Date)

class AstroMonth(Base):
    """ 星座运势 月数据 """
    __tablename__ = 'astro_month'
    id = Column(Integer, primary_key=True)
    astroid = Column(SMALLINT)
    name = Column(String(20))
    summary = Column(String(500))
    health = Column(String(500))
    love = Column(String(500))
    money = Column(String(500))
    career = Column(String(500))
    date = Column(Integer)

class AstroYear(Base):
    """ 星座运势 年数据 """
    __tablename__ = 'astro_year'
    id = Column(Integer, primary_key=True)
    astroid = Column(SMALLINT)
    name = Column(String(20))
    summary = Column(String(1000))
    career = Column(String(1000))
    love = Column(String(1000))
    money = Column(String(1000))
    date = Column(CHAR(4))  # 年份


class Lunar(Base):
    """ 农历 """
    __tablename__ = 'lunar'
    id = Column(Integer, primary_key=True)
    year = Column(SMALLINT)
    month = Column(SMALLINT)
    day = Column(SMALLINT)
    lunarYear = Column(SMALLINT)
    lunarMonth = Column(SMALLINT)
    lunarDay = Column(SMALLINT)
    cnyear = Column(String(10))
    cnmonth = Column(String(10))
    cnday = Column(String(10))
    hyear = Column(String(10))
    cyclicalYear = Column(String(10))
    cyclicalMonth = Column(String(10))
    cyclicalDay = Column(String(10))
    suit = Column(String(100))
    taboo = Column(String(100))
    animal = Column(String(10))
    week = Column(String(10))
    festivalList = Column(String(100))
    jieqi = Column(String(20))
    maxDayInMonth = Column(SMALLINT)
    leap = Column(SMALLINT)
    lunarYearString = Column(String(20))
    bigMonth = Column(SMALLINT)


class Star(Base):
    """ 明星资料 """
    __tablename__ = 'star'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    name_initial = Column(String(50))
    name_spell = Column(String(50))
    profession = Column(String(50))
    area = Column(String(50))
    height = Column(String(20))
    weight = Column(String(20))
    birthday = Column(String(20))
    astro = Column(String(10))
    bloodtype = Column(String(10))
    intro = Column(String(500))
    avatar = Column(String(500))

class Weather(Base):
    """ 天气数据 """
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    city = Column(String(20))
    shidu = Column(String(10))
    pm25 = Column(String(10))
    pm10 = Column(String(10))
    wendu = Column(SMALLINT)
    sunrise = Column(String(10))
    sunset = Column(String(10))
    high = Column(String(20))
    low = Column(String(20))
    aqi = Column(SMALLINT)
    quality = Column(String(20))
    fx = Column(String(20))
    fl = Column(String(20))
    stype = Column(String(20))
    notice = Column(String(100))