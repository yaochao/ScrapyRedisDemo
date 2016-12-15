#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yaochao on 2016/12/14
import json

from scrapy_redis.spiders import RedisSpider
from scrapy import Request, Selector

class BaikeSpider(RedisSpider):
    name = 'baike'

    custom_settings = {
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'REDIS_URL': 'redis://121.42.202.198:6379',
        'ITEM_PIPELINES': {
            'ScrapyRedisDemo.pipelines.BaikeMongodbPipeline': 100
        }
    }

    def parse(self, response):
        results = response.xpath('//a/@href').extract()
        results = ['http://baike.baidu.com' + x for x in results if '/view/' in x]
        for url in results:
            request = Request(url=url, callback=self.parse)
            yield request
        title = response.xpath('//dd/h1/text()').extract_first()
        url = response.url
        selector = Selector(response)
        newLemmaId = selector.re(r'newLemmaIdEnc:"(.*?)"')[0] if selector.re(r'newLemmaIdEnc:"(.*?)"') else ''
        item = {
            '_id': newLemmaId,
            'title':title,
            'url': url,
            'newLemmaId': newLemmaId,
        }
        if newLemmaId:
            request = Request(url='http://baike.baidu.com/api/lemmapv?id=' + newLemmaId, callback=self.parse_pageview)
            request.meta['item'] = item
            yield request

    def parse_pageview(self, response):
        item = response.meta['item']
        a_dict = json.loads(response.text)
        item['pv'] = a_dict['pv']
        yield item
        # print item
