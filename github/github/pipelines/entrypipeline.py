# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from hashlib import md5
import requests
import logging

from scrapy.exceptions import DropItem
from github import settings


class DuplicatesPipeline(object):

    def process_item(self, item, spider):
        github_url      = item['github_url']
        identified_code = md5(github_url).hexdigest()
        url             = settings.SERVER_URL
        check_url       = "{base_url}{id_code}".format(
            base_url=url,
            id_code=identified_code,
        )
        res             = requests.head(check_url)
        if res.status_code == 200:
            raise DropItem(item)
        else:
            return item


class PostProjectPipeline(object):

    def process_item(self, item, spider):
        url = settings.SERVER_URL
        res = requests.post(url, json=dict(item))
        if res.status_code == 201:
            print ("OK")



# class DuplicatesPipeline(object):
#
#     def process_item(self, item, spider):
#         check_url           = "{url}{identified_code}".format(
#             url = settings.SERVER_URL,
#             identified_code = item['asin'],
#         )
#         res = requests.head(check_url)
#         if res.status_code  == 200:
#             raise DropItem("Duplicate entity found: %s", item)
#         else:
#             return item


# class PostEntityPipeline(object):
#
#     def process_item(self, item, spider):
#         image_path          = [row['path'] for row in item['images']]
#         item['image_urls']  = image_path
#         res = requests.post(settings.SERVER_URL, json=dict(item))
#         if res.status_code == 201:
#             return item
#         else:
#             logging.error(res.text)
#


