# -*- coding: utf-8 -*-

import logging, datetime, time, os

def slog(level, msg, *args, **kwargs):
    LEVEL_MAP = {
        'D': logging.DEBUG,
        'I': logging.INFO,
        'W': logging.WARNING,
        'E': logging.ERROR
    }
   
    # if type(msg) == str and os.name == 'nt':
    #     msg = msg.decode('utf-8').encode('gb2312')

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

def weather_data_check(provinces):
    """ 天气数据检查， 返回要爬取的城市索引 """
    from mkspider.lib.db import session
    from mkspider.lib.models import Weather
    
    curr_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 查询当前日期最后一个城市名称
    date_weather = session.query(Weather).filter_by(
        date=curr_date).order_by(Weather.id.desc()).first()
    if date_weather:
        city = str(date_weather.city.decode('utf-8'))
        # 判断当前日期是否查询
        city_last_weather = session.query(Weather).filter_by(
            city=city).order_by(Weather.date.desc()).first()
        if city_last_weather and str(city_last_weather.date) == date_operate(curr_date, 4):
            return provinces.index(city) + 1
    return 0

def date2str(arr):
    """对象转字符串"""
    for item in arr:
        for field in item:
            if isinstance(item[field], datetime.datetime):
                item[field] = item[field].strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(item[field], datetime.date):
                item[field] = item[field].strftime("%Y-%m-%d")

    return arr

def send_email(title, content, logger=None):
    """ 发送邮件 """
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 发送邮箱
    sender = '1019912599@qq.com'
    # 接收邮箱，可以是多个
    receivers = ['1348207308@qq.com']

    # 发送邮件服务器
    mail_host = 'smtp.qq.com'
    mail_user = sender
    mail_pass = 'gcqgfvefuwlvbcha'

    # 三个参数：第一个为文本内容，第二个设置文本格式，第三个utf-8编码
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header('mkspider', 'utf-8') # 发送者名称
    message['To'] = Header('lengfeng', 'utf-8')   # 接收者名称
    message['Subject'] = Header(title, 'utf-8')   # 标题

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        if logger:
            logger.info('%s:邮件发送成功' % title)
    except smtplib.SMTPException:
        if logger:
            logger.error('%s:邮件发送失败' % title)

if __name__ == '__main__':
   send_email('测试邮件', '测试内容.....')