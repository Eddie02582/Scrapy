# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import urllib
import codecs 

class ExamplePipeline(object):
    def process_item(self, item, spider):
        return item

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        

class DownLoad(ImagesPipeline):
    # def __init__(self):  
        # self.file = codecs.open('news.json', 'wb', encoding='utf-8')  
        
    def get_media_requests(self, item, info):
        #if item['img_urls']:
        Count = 1
        save_path = "D:\\crawl\\{0}\\'{1}'".format(item['board'],item['title']) 
        create_folder(save_path)        

        file = codecs.open('beauty.json', 'wa', encoding='utf-8')  
        line = json.dumps(dict(item)) + '\n'         
        file.write(line.decode("unicode_escape"))   
        
        for image_url in item['image_urls']:	
            urllib.request.urlretrieve(image_url,save_path + '\\%s.jpg' %Count)
            Count+=1
        
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]    
        if not image_paths:
            raise DropItem("Item contains no images")       
        #item['image_paths'] = image_paths   

        return item	  
        
        

        
        
        