# Scrapy

## 安裝
首先 pip install scrapy </br>
如果出現vc++錯誤,可到<a href="https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted ">Unofficial Windows Binaries for Python Extension Packages </a> 抓取對應的twisted 安裝</br>
接著再 pip install scrapy </br>


## 建立案子
指令為
```
    scrapy startproject [name]
```
 
在cmd下   scrapy startproject example會產生

```
example/
    scrapy.cfg            # deploy configuration file

    example/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```            


## 開始爬蟲
example/spiders 在建立spider.py內容如下
<ul>
    <li>name:定義爬蟲的名字</li>
    <li>allowed_domains:定義允許的網域(可不填)</li>
    <li>start_urls:要爬蟲的網頁</li>
    <li>parse(response):解析網址(會對每個start_url 執行parse)</li>
</ul>

這個範例為簡單把網頁的body存在本地

```
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['example.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',     
    ] 

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


```
## Extracting data


```
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['example.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',     
    ] 

    def parse(self, response):
        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").extract_first()
            author = quote.css("small.author::text").extract_first()
            tags = quote.css("div.tags a.tag::text").extract()
            print(dict(text=text, author=author, tags=tags))
```

## Import data as .json

使用yield疊代儲存數據
```
    def parse(self, response):   
        for quote in response.css("div.quote"):
            yield {
                text :quote.css("span.text::text").extract_first(),
                author :quote.css("small.author::text").extract_first(),
                tags :quote.css("div.tags a.tag::text").extract(),
           
        }
```
執行下列指令
```
scrapy crawl example -o quotes.json
```

## Following links
介紹如何連續取每一頁
找到網頁最下面next

```html
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```
透過css/xpath取得href
```
>>> response.css('li.next a::attr(href)').extract_first()
'/page/2/'

>>> response.xpath('//li[contains(@class, "next")]//a/@href').extract_first()
'/page/2/'
```

因為這網頁只有一個li,所以xpath 可以簡化
```
>>> response.xpath('//li//a/@href').extract_first()
'/page/2/'
```

spider.py
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

使用response.follow ,主要差異在於response.follow 支持相對路徑

```
    def parse(self, response):   
        .....
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)            
```






