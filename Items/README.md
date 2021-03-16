# Items


在item.py新增
```python 
class QuotesItem(scrapy.Item):
	text = Field()  
	author = Field()  
	tags = Field() 
```
spider.py如下

注意使用yield Item 就不能使用下面指令,需要額外寫Pipelines輸出
```
scrapy crawl quotes -o qoutes.csv
```

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

0
