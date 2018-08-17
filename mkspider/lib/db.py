# -*- coding: utf-8 -*-
"""历史上的今天数据解析脚本"""

import os
import sys
# bin_dir = os.path.dirname(os.path.realpath(__file__))
# root_dir = os.path.join(bin_dir, '..', 'mkspider')
# sys.path.append(root_dir)

from mkspider.settings import DB_CONFIG
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mkspider.lib.models import Histoday

# 创建数据库引擎
engine = create_engine(DB_CONFIG, encoding="utf-8", echo=False)

# 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session_class = sessionmaker(bind=engine)
# 生成session实例
session = Session_class()

