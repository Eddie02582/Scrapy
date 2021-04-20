# 爬取動態網頁
使用Spalsh,Spalsh提供JavaScript渲染服務，它是一個使用Twisted和QT5在Python中實現的支持HTTP API調用的輕量級的web瀏覽器。


可以參考<a href = "https://splash-cn-doc.readthedocs.io/zh_CN/latest/scrapy-splash-toturial.html">官方文檔</a>

## install
```
   pip install scrapy-splash
```
## 配置
使用docker 配置比較簡單

### Pull Image
```
   docker pull scrapinghub/splash
```

### Run
```
   docker run -p 8050:8050 scrapinghub/splash
```

## 修改scrapy setting.py設定

Splash服務的地址
```
SPLASH_URL = 'http://127.0.0.1:8050'
```

DOWNLOADER_MIDDLEWARES 加上splash的中間件，並設置 HttpCompressionMiddleware 對象的優先級

```python 
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
```

設定
```python
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
```

設定DUPEFILTER_CLASS
```python
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
```

您可以设置scrapy.contrib.httpcache.FilesystemCacheStorage 来使用Splash的HTTP缓存
```python
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```



## code
參考<a href = "https://github.com/Eddie02582/Scrapy/tree/master/%5BScrapy%20%E6%95%99%E5%AD%B84%5D%E7%88%AC%E8%9F%B2%E6%92%B0%E5%AF%AB">[Scrapy 教學4]爬蟲撰寫</a>
首先使用start_requests取代start_urls

```python
    def start_requests(self):  
        url = "http://quotes.toscrape.com/js/"
        yield scrapy.Request(url) 
```

將scrapy.Request 取代成SplashRequest


```python
import scrapy
from scrapy_splash import SplashRequest
class QuotesJsSpider(scrapy.Spider):
    name = "quotesjs"   

    def start_requests(self):     
        url = 'http://quotes.toscrape.com/js/'
        yield SplashRequest(url, self.parse, args={'wait': 0.5})
                
    
    def parse(self, response):   
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield SplashRequest(next_page, callback = self.parse)

```











