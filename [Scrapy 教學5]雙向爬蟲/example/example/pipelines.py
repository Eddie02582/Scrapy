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

class ExamplePipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('quotes.item', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        #line = json.dumps(dict(item)) + "\n"
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
        
        
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_filename(path):
    return path.split('/')[-1]


class DownLoad(ImagesPipeline):
    def get_media_requests(self, item, info):
        save_path = "D:\\crawl\\{0}\\{1}\\".format(item['board'],item['title']) 
        create_folder(save_path)        

        for image_url in item['image_urls']:	
            urllib.request.urlretrieve(image_url,save_path + get_filename(image_url))
            
        
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]    
        if not image_paths:
            raise DropItem("Item contains no images")        
        return item	     
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        