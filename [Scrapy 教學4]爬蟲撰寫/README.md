# [Scrapy 教學4]爬蟲撰寫

在前面教學如何使用CSS或是Xpath來取得資料,接下來是實現,首先取得每個div.quote的selector接著使用迴圈去取值

## simple scrapy
```python
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

```
## scrapy with next page
如果我們要爬許多的網頁,可以透過增加start_urls,但是有時候我們不知道實際有幾頁,可以透過另一種方式<br>
首先是將鏈接提取到我們要關注的頁面。檢查我們的頁面，可以看到帶有以下標記的指向下一頁的鏈接

```html
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```

使用css取得next page link
```python
>>> response.css('li.next a::attr(href)').get()
'/page/2/'
```


在最下方添加抓取下一頁的連結,如果有就使用yield scrapy.Request(absolute_url, callback = self.parse)繼續請求
由於scrapy.Request需要絕對路徑,透過urljoin轉換成絕對路徑

```python
import scrapy
from example.items import QuotesItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }


        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)
```

也可以使用response.follow,好處是可以直接傳入select

```python 
    def parse(self, response):  
        for quote in response.css("div.quote"):  
            yield {
                'text' : quote.css("span.text::text").extract_first(),
                'author' : quote.css("small.author::text").extract_first(),
                'tags' : quote.css("div.tags a.tag::text").extract(),
            
            }  
        
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, callback=self.parse)

```



對於tag 為a元素，response.follow會自動使用其href屬性,因此可以在改寫成如下

```python 
for a in response.css('li.next a'):
    yield response.follow(a, callback=self.parse)
```

對於multiple requests可以使用response.follow_all

```python 
anchors = response.css('ul.pager a')
yield from response.follow_all(anchors, callback=self.parse)
```

或者
```python 
yield from response.follow_all(css ='ul.pager a', callback = self.parse)
```






