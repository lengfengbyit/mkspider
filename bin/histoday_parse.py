# -*- coding: utf-8 -*-
"""历史上的今天数据解析脚本"""

import os, sys
bin_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(bin_dir, '..')
sys.path.append(root_dir)

from mkspider.lib.db import engine, session
from mkspider.lib.models import Histoday

def get_date(datestr):
    """ 获得date格式 """
    if not datestr:
        return False

    datestr = datestr.strip()
    date_len = len(datestr)
    year = datestr[0:4]
    if date_len == 8:
        month = datestr[4:6]
        day = datestr[6:8]
    elif date_len == 7:
        if int(datestr[0:2]) > 20:
            year = datestr[0:3]
            month = datestr[3:5]
            day = datestr[5:7]
        else:
            month = '0%s' % datestr[4:5]
            day = datestr[5:7]
    else:
        return False

    return {
        'year': year,
        'month': month,
        'day': day,
        'date': '-'.join([year, month, day])
    }

def save_to_db(data):
    """ 数据保存到数据库 """ 
    if not data:
        return False

    datas = []
    for item in data:
        datas.append(
            Histoday(**item)
        )

    session.add_all(datas)
    session.commit()

def read_file_line(file_path):
    """ 读取一行解析一行 """
    # 存储读取到的数据
    data = []
    totalCount = 0
    index = 0
    with open(file_path, 'r', encoding="utf-8") as f:
        line = f.readline()
        item = {}
        while line:
            index += 1
            if line.startswith('﻿#') or line.startswith('##'):

                line = line.strip('﻿#')
                try:
                    spaceIndex = line.index(' ')
                    datestr = line[0:8]
                    title = line[8:]
                except Exception as e:
                    print('----[标题处理错误]%s' % line)
                    sys.exit(0)

                if item:
                    tmp = item.copy()
                    data.append(tmp)
                    item = {}
                    dataCount = len(data)
                    if dataCount >= 1000:
                        save_to_db(data)
                        totalCount += dataCount
                        data = []

                item['title'] = title
                dateInfo = get_date(datestr)

                if dateInfo:
                    item.update(dateInfo)
                else:
                    print('[日期获取失败]:%s' % title)
            elif item:
                if 'content' not in item:
                    item['content'] = ''

                item['content'] = "%s%s/n" % (item['content'], line)

            if index % 1000 == 0:
                print('----------处理行数：%s' % index)

            # 获得下一行内容
            line = f.readline()

        if item:
            data.append(item)

        dataCount = len(data)
        if dataCount > 0:
            save_to_db(data)
            totalCount += dataCount

        print("数据条数:%s" % totalCount)

def read_file_all(file_path, tags):
    """ 先把文件全部读取出来在解析 """
    with open(file_path, 'r', encoding="utf-8") as f:
        file_data = f.read().split('##')

        index = 0
        data = []
        for item in file_data:
            index += 1
            if index == 1:
                continue
            
            try:
                # 第一行结束位置
                first_line_end_index = item.index('\n')
                first_line = item[0:first_line_end_index]
                # 获得第一个空格的位置
                first_space_index = item.index(' ')
                datestr = first_line[0:first_space_index].strip()
                title = first_line[first_space_index:].strip()
                dateInfo = get_date(datestr)
            except Exception as e:
                print(str(e))
                print(item)
                exit(0)
          
            tmp = {
                'title': title,
                'content': item[first_line_end_index:],
                'tags': tags[title] if title in tags else ''
            }
           
            tmp.update(dateInfo)
            data.append(tmp)

            if len(data) >= 1000:
                save_to_db(data)
                data = []
                print('----------处理行数：%s' % index)

        if data:
            save_to_db(data)
            print('----------处理行数：%s' % index)

def read_file_tags(file_path):
    """ 读取标签信息 """

    tags_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        tags = f.read().split("\n")
        for item in tags:
            try:
                title, tag = item.split('::')
                tags_map[title] = tag
            except Exception as e:
                print(item)
                print(str(e))
                exit(0)
            
        return tags_map
        
if __name__ == '__main__':
    # 文件路径
    file_path = os.path.join(bin_dir, '..', 'data/histoday.txt')
    tags_file_path = os.path.join(bin_dir, '..', 'data/tags.txt')
    # read_file_line(file_path)

    tags = read_file_tags(tags_file_path)
    read_file_all(file_path, tags)
