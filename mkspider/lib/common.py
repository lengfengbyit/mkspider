# -*- coding: utf-8 -*-

import logging, datetime

def slog(level, msg, *args, **kwargs):
    LEVEL_MAP = {
        'D': logging.DEBUG,
        'I': logging.INFO,
        'W': logging.WARNING,
        'E': logging.ERROR
    }

    if 'decode' in msg:
        msg = msg.decode('utf-8').encode('gb2312')

    if level not in LEVEL_MAP:
        print(msg)
    else:
        logging.log(LEVEL_MAP[level], msg, *args, **kwargs)


def get_weekth_by_date(date, return_type='weekth', limit='-'):
    """ 获得指定日期是第几周 """
    if not date:
        return 0

    year, month, day = str(date).split(limit)

    # 返回数据格式：(2017, 52, 7)  年，年的第几周，第几周的第几天
    res = datetime.date(int(year), int(month), int(day)).isocalendar()

    if not res:
        return False

    if return_type == 'year':
        return res[0]
    elif return_type == 'weekth':
        return res[1]
    elif return_type == 'dayth':
        return res[2]
    else:
        return res


def date_operate(date, days = 1, limit='-'):
    """ 日期运算，
        date: 要计算的原始日期
        days: 加减的天数，可以使正数也可以是负数
        limit: 日期的分隔符
    """
    if not date:
        return False

    year, month, day = date.split(limit)
    next_date = datetime.datetime(int(year), int(
        month), int(day)) + datetime.timedelta(days=days)

    return next_date.strftime('%Y{}%m{}%d'.format(limit,limit))

def default_val(data, key, default_val=''):
    """ 获取值并设置默认值 """
    return data[key] if key in data else default_val

if __name__ == '__main__':
   
   date = date_operate('2018-08-20', 4)
   print(date)
