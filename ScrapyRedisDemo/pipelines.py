# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class ScrapyredisdemoPipeline(object):
    def process_item(self, item, spider):
        return item

class BaikeMongodbPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host='121.42.202.198', port=27017)
        db = client['baidu_baike']
        self.info = db['info']

    def process_item(self, item, spider):
        try:
            self.info.insert(item)
        except:
            print('insert into mongodb error!!!')
        return item
