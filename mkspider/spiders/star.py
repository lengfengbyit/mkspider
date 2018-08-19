# -*- coding: utf-8 -*-
# 明星资料爬虫
import scrapy, math
from mkspider.lib.db import session
from mkspider.lib.models import Star
from mkspider.items import Star as StartItem


class StarSpider(scrapy.Spider):
    name = 'star'
    allowed_domains = ['www.ylq.com']
    start_urls = ['http://www.ylq.com/star/list-all-------%s.html']
    # 页数
    page = 1
    # 每页60个
    page_size = 60
    # 当页的第几个
    index = 1
    # 'http://www.ylq.com/star/list-all-------1.html'
    def start_requests(self):
        total_count = session.query(Star).count()
        if total_count > 0:
            self.index = total_count % self.page_size + 1
            self.page = math.floor(total_count / self.page_size) + 1

        return [scrapy.Request(self.next_url())]


    def parse(self, response):

        li_list = response.xpath("//div[@class='fContent']/ul/li")
        for item in li_list:

            avatar = item.xpath('./a/img/@src').extract_first()
            name = item.xpath('./a/h2/text()').extract_first()
            detail_url = item.xpath('./a/@href').extract_first()

            request = scrapy.Request(detail_url, callback=self.parse_detail)
            request.meta['avatar'] = avatar
            request.meta['name'] = name
            yield request

        self.page += 1
        self.index = 1
        yield scrapy.Request(self.next_url())

    def parse_detail(self, response):
        info=response.xpath("//div[@class='perData']/div[@class='sLeft']")
        li_list = info.xpath('./ul/li')

        fields = ['area', 'height', 'weight', 'birthday', 'astro', 'bloodtype']
        start_item = StartItem()
        # 职业
        start_item['profession'] = info.xpath('./h1/span/text()').extract_first()
        start_item['intro'] = info.xpath("./p[@class='intro']/text()").extract_first()
        start_item['name'] = response.meta['name']
        start_item['avatar'] = response.meta['avatar']

        for field in fields:
            i = fields.index(field)
            a_text = li_list[i].xpath('./a/text()')
            if a_text:
                start_item[field] = a_text.extract_first()
            else:
                start_item[field] = li_list[i].xpath('./text()').extract_first()

        yield start_item






    def next_url(self):
        return self.start_urls[0] % self.page
