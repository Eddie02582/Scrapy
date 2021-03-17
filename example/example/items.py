# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QuotesItem(scrapy.Item):
	text = scrapy.Field()  
	author = scrapy.Field()  
	tags = scrapy.Field() 
    
class PttItem(Item):
    board = Field()  
    author = Field()  
    title = Field()
    date_time = Field()    
    content = Field()

    image_urls = Field()
    images = Field()
    image_paths = Field()