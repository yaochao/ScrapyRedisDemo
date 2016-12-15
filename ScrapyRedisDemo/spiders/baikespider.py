#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/12/14

from scrapy_redis.spiders import RedisSpider
from scrapy import Request

class BaikeSpider(RedisSpider):
    name = 'baike'

    custom_settings = {
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'REDIS_URL': 'redis://121.42.202.198:6379'
    }

    def parse(self, response):
        results = response.xpath('//a/@href').extract()
        results = ['http://baike.baidu.com' + x for x in results if '/view/' in x]
        for url in results:
            request = Request(url=url, callback=self.parse)
            yield request
        title = response.xpath('//dd/h1/text()').extract_first()
        print(title)
