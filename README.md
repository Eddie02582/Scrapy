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




