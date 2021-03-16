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




















