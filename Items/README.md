# Items
抓取的主要目的是從非結構化源（通常是網頁）中提取結構化數據。 Scrapy Spider可以將提取的數據作為Python字典返回。<br> 
Python字典雖然方便且熟悉，但缺乏結構：很容易在字段名稱中輸入錯誤或返回不一致的數據，尤其是在具有許多蜘蛛的大型項目中。<br> 

在item.py新增
```python 
class QuotesItem(scrapy.Item):
	text = Field()  
	author = Field()  
	tags = Field() 
```
spider.py如下


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
