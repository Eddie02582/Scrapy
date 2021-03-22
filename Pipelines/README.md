# Pipelines
pipelines 主要定義data export 格式

## CSV
pipelines.py
```python
import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
		
```
spider.py 使用方法
新增 custom_settings = {'ITEM_PIPELINES': {'example.pipelines.CSV': 800,}}

```python
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    max_pages = 3
    pages = 0
    custom_settings = {'ITEM_PIPELINES': {'example.JsonWriterPipeline.CSV': 800,}}  
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]  

    def parse(self, response):  
        for quote in response.css("div.quote"):  
            yield {
                'text' : quote.css("span.text::text").extract_first(),
                'author' : quote.css("small.author::text").extract_first(),
                'tags' : quote.css("div.tags a.tag::text").extract(),
            
            }
            
            next_page = response.css('li.next a::attr(href)').extract_first()
        self.pages += 1	
        
        if next_page is not None and self.pages < self.max_pages:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

```


## Downdload Image


```
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
        
```














