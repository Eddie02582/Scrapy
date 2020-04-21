# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class QuotesItem(scrapy.Item):
	text = Field()  
	author = Field()  
	tags = Field() 

	
class PttItem(Item):
    board = Field()  
    author = Field()  
    title = Field()
    date_time = Field()    
    content = Field()

    image_urls = Field()
    images = Field()
    image_paths = Field()
