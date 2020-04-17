# Following links
介紹如何結取每個分頁,一樣以http://quotes.toscrape.com/page/1/為例


## 利用css /xpath 取得下一頁的網址

```html
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```

### css
```
>>> response.css('li.next a::attr(href)').extract_first()
'/page/2/'
```

### xpath
```
>>> response.xpath('//li[contains(@class, "next")]//a/@href').extract_first()
'/page/2/'
```

這網頁只有一個li,所以xpath 可以簡化
```
>>> response.xpath('//li//a/@href').extract_first()
'/page/2/'
```

## yield scrapy.Request
利用yield scrapy.Request(next_page, callback = self.parse)

```
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # allowed_domains = ['example.com']
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

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```
## response.follow
主要差異在於response.follow 支持相對路徑

```
    def parse(self, response):   
        .....
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)            
```


## 指定爬前幾頁

```
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    max_pages = 3
    pages = 0
    # allowed_domains = ['example.com']
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



