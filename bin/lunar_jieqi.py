# -*- coding: utf-8 -*-
""" 提取日历数据中节气数据放到节气字段中 """


import os, sys, json
bin_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(bin_dir, '..')
sys.path.append(root_dir)

from mkspider.lib.db import session
from mkspider.lib.models import Lunar
from mkspider.lib.common import slog

lanurs = session.query(Lunar).order_by(Lunar.id.asc()).all()

for item in lanurs:
    jieqi_data  = json.loads(item.jieqi)
    day = str(item.day)
    if day in jieqi_data and not item.jieqi2:
        slog("DD", "[%s-%s-%s]节气:%s" %
             (item.year, item.month, item.day, jieqi_data[day]))
        session.query(Lunar).filter_by(id=item.id).update({'jieqi2': jieqi_data[day]})

session.commit()

