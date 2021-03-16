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
 
在cmd下   scrapy startproject example 會產生

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

## 簡單的爬蟲


start_urls: starts url array<br>
parse: 解析網頁資料<br>
name :cmd 執行爬蟲的名字
 
```python 
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
 

 cmd 執行
 ```
    scrapy crawl quotes -o 123.csv 
 ```
 
 ## Start Learning
 
 <ul>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Extracting%20data">Extracting data</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Items">Items</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Pipelines">Pipelines</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Following%20links">Following links</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Two-direction%20Crawling">Two-direction Crawling</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/PTT%20Spider">Crawl PTT</a></li>
</ul>
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 