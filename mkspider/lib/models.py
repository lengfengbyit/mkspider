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
    presummary = Column(String(200))
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
    health = Column(String(200))
    job = Column(String(200))
    love = Column(String(200))
    money = Column(String(200))
    career = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)

class AstroMonth(Base):
    """ 星座运势 月数据 """
    __tablename__ = 'astro_month'
    id = Column(Integer, primary_key=True)
    astroid = Column(SMALLINT)
    name = Column(String(20))
    summary = Column(String(500))
    health = Column(String(200))
    love = Column(String(200))
    money = Column(String(200))
    career = Column(String(200))
    date = Column(Integer)

class AstroYear(Base):
    """ 星座运势 年数据 """
    __tablename__ = 'astro_year'
    id = Column(Integer, primary_key=True)
    astroid = Column(SMALLINT)
    name = Column(String(20))
    summary = Column(String(300))
    career = Column(String(300))
    love = Column(String(300))
    money = Column(String(300))
    date = Column(CHAR(4))  # 年份
