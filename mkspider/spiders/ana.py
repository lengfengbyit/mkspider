# -*- coding: utf-8 -*-
""" 名言警句爬虫 """

import scrapy, json
from mkspider.items import Ana
import logging, sys


class AnaSpider(scrapy.Spider):
    name = 'ana'
    allowed_domains = ['hanyu.baidu.com']
    start_urls = [
        'https://hanyu.baidu.com/hanyu/ajax/motto_list?wd=%E5%90%8D%E8%A8%80&from=poem&userid=745990104&ptype=motto&pn=1']
    
    base_url = "https://hanyu.baidu.com/hanyu/ajax/motto_list?wd=%E5%90%8D%E8%A8%80&from=poem&userid=745990104&ptype=motto&pn="
    
    page = 1
    totalPage = 4956
    
    def parse(self, response):
        logging.info('------curr page:%s' % self.page)
        json_data = json.loads(response.body)
        if 'ret_array' in json_data:
            for item in json_data['ret_array']:
                try:
                    ana = Ana()
                    ana['title'] = item['name'][0]
                    ana['author'] = ''
                    ana['froms'] = ''
                    if 'author' in item:
                        ana['author'] = item['author'][0]
                    if 'from' in item:
                        ana['froms'] = item['from'][0]
                    ana['tags'] = ",".join(item['tag'])
                    ana['like_count'] = int(item['like_count'])
                    ana['dislike_count'] = int(item['dislike_count'])
                except Exception as e:
                    logging.error(str(e))
                    print(item)
                    sys.exit(0)
                    continue
                yield ana 
        
        self.page += 1
        if self.page <= self.totalPage:
            next_link = self.base_url + str(self.page)
            yield scrapy.Request(next_link)
