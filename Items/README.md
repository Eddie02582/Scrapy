# Items

```
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
```

## Items
改用Items寫法

在item.py新增
```python 
class QuotesItem(scrapy.Item):
	text = Field()  
	author = Field()  
	tags = Field() 
```

spider.py

```python 
import scrapy
from example.items import QuotesItem
class QuotesSpider(scrapy.Spider):
    name = "quotes"  
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        
    ]   
    def parse(self, response):  
        for quote in response.css("div.quote"):  
            Item = QuotesItem()
            Item['text'] = quote.css("span.text::text").get(),
            Item['author'] = quote.css("small.author::text").get()
            Item['tags'] = quote.css("div.tags a.tag::text").extract()              
            yield Item
            
        next_page = response.css('li.next a::attr(href)').extract_first()   
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)  
            
```

## Items Loader