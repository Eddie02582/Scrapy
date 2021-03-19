# Scrapy

## 安裝
首先 pip install scrapy </br>

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

## 爬蟲的格式


start_urls: 要爬蟲的網址<br>
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
        pass
 ```


## How to extract data
使用scrapy shell 來學習或測試,指令為
```
   scrapy shell url
```
這邊以http://quotes.toscrape.com/page/1/為例<br>



可以從網頁原始碼觀察,每個block 都被div class="quote"包住
```html
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```
主要可以使用css 或是xpath 來select element


### css selector 

#### get tag elements 



取得div class = "quote" 底下所有span class = "text"
```python
response.css('div.quote span.text')
>>>[<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]/...
```

#### get list string (extract /getall)
```python
>>> response.css('div.quote span.text').getall()
['<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>', 
 '<span class="text" itemprop="text".....>
]
```






 cmd 執行
 ```
    scrapy crawl quotes -o 123.csv 
 ```
 
 ## Start Learning
 
 <ul>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Extracting%20data">Extracting data</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Following%20links">Following links</a></li>    
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Items">Items</a></li>    
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Pipelines">Pipelines</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/Two-direction%20Crawling">Two-direction Crawling</a></li>
    <li><a href = "https://github.com/Eddie02582/Scrapy/tree/master/PTT%20Spider">Crawl PTT</a></li>
</ul>
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 