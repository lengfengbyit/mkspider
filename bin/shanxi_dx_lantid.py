# -*- coding: utf-8 -*-
""" 提取陕西号段所属地市编码 """

import os

# 陕西所有地市
areas = [
    '西安','咸阳','渭南','延安','宝鸡','榆林','铜川','汉中','安康','商洛'
]

curr_dir = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(curr_dir, '..', 'data', 'shanxi_lantid')
res_file_path = os.path.join(dir_path, 'shanxi_lantid3.txt')

# 获得所有文件名
files = os.listdir(dir_path)
res = []

# 已有的lantid用于过滤
maplist = []

for file_name in files:
    f_path = os.path.join(dir_path, file_name)
    with open(f_path, 'r', encoding='utf-8') as f:
        texts = f.read().split('\n')
        if not texts:
            continue
        for line in texts:
            if not line:
                continue
            fields = line.split(',')
            if len(fields) != 3 or not fields[0].isdigit() or fields[2] not in areas:
                continue

            # res.append(line)
            res.append(fields)


with open(res_file_path, 'w+', encoding='utf-8') as f:
    # text = '\n'.join(res)
    
    # 这里是为了去重
    field_map = {}
    for fields in res:
        field_map[fields[0]] = fields[1]

    lines = []
    for field in field_map:
        if int(field) in maplist:
            continue
        line = '{} => {},'.format(field, field_map[field])
        lines.append(line)
    
    text = '\n'.join(lines)
    f.write(text)
