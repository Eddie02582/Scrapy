# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import urllib.request
import codecs 

class TidyUpPipeline:
    def process_item(self, item, spider):
        item['date'] = map(datetime.isoformat, item['date'])        
        return item

def imgur_link_to_url(link):    
    import re
    match = re.match('^//imgur.com/([a-zA-Z0-9]+)',link)
    if match:
        return "https://i.imgur.com/" + match.group(1) + ".jpg"
    else:
        return link    

class ImgurPipeline:
    def process_item(self, item, spider):
        if 'image_urls' in item:
            item['image_urls'] = list(map(imgur_link_to_url, item['image_urls']))
        return item



def get_filename(path):
    return path.split('/')[-1]
       

import scrapy
class PttImageDownLoad(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:	          
            yield scrapy.Request(
              image_url,
              meta={
                'title': item['title'],
                'board': item['board'],
                'file_name': get_filename(image_url) 
              }
            )

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        file_name = request.meta['file_name']
        title = request.meta['title']
        board = request.meta['board']
        path = "D:\\crawl\\{0}\\{1}\\".format(board,title)
        return path + file_name
        
        
        
        
        
        
        
        
        
        