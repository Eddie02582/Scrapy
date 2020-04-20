# Following links
介紹如何結取每個分頁,一樣以http://quotes.toscrape.com/page/1/為例


## How to get data form following links
首先是將鏈接提取到我們要關注的頁面。檢查我們的頁面，可以看到帶有以下標記的指向下一頁的鏈接：

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

也可以使用attrib 屬性取得
```python
>>> response.css('li.next a').attrib['href']
'/page/2/
```



使用yield scrapy.Request(absolute_url, callback = self.parse)
可以將網址在傳入parse() 再執行



```python 
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
            yield scrapy.Request(next_page, callback = self.parse)
```

response.urljoin(),會將網址轉成絕對路徑　<br>


## A shortcut for creating Requests

使用response.follow取代scrapy.Request,response.follow 支持相對路徑,可以省略response.urljoin這行

```python 
    def parse(self, response):   
        .....
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)            
```
也可以支援傳入selector
```python 
    def parse(self, response):  
        for quote in response.css("div.quote"):  
            yield {
                'text' : quote.css("span.text::text").extract_first(),
                'author' : quote.css("small.author::text").extract_first(),
                'tags' : quote.css("div.tags a.tag::text").extract(),
            
            }  
        
        for href in response.css('ul.pager a::attr(href)'):
            yield response.follow(href, callback=self.parse)

```



對於<a>元素，有一個快捷方式：response.follow自動使用其href屬性。 因此，代碼可以進一步縮短：

```python 
for a in response.css('ul.pager a'):
    yield response.follow(a, callback=self.parse)
```

對於multiple requests可以使用response.follow_all

```python 
anchors = response.css('ul.pager a')
yield from response.follow_all(anchors, callback=self.parse)
```

或者
```python 
yield from response.follow_all(css='ul.pager a', callback=self.parse)
```


















