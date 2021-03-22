# PTT Spider


## Beauty


### 抓取Link
這是一個雙向爬蟲,需要界面的下一頁,和每頁每個文章的Link

<img src = "1.PNG"></img>
首先抓取下一頁的連結

```html
<div class="btn-group btn-group-paging">
	<a class="btn wide" href="/bbs/Beauty/index1.html">最舊</a>
	<a class="btn wide" href="/bbs/Beauty/index3272.html">‹ 上頁</a>
	<a class="btn wide disabled">下頁 ›</a>
	<a class="btn wide" href="/bbs/Beauty/index.html">最新</a>
</div>
```

從這邊來看只需要抓取tag 為a,class 為wide底下第2個link


使用scrapy shell 來測試,因為進去網頁會跳出是否滿18,所以直接使用scrapy shell
```
url = 'https://www.ptt.cc/bbs/Beauty/index.html'
cookies = {"over18": "1"}
response = scrapy.Request(url, cookies=cookies)
fetch(response)
```
下完後就可以來測試,以css為例
```python
>>> response.css('a.wide').extract()[1]
'<a class="btn wide" href="/bbs/Baseball/index10010.html">‹ 上頁</a>'
```

抓取文章連結

```html
<div class="r-ent">
	...
	<div class="title">			
		<a href="/bbs/Beauty/M.1587404155.A.04D.html">[正妹] 峮峮</a>			
	</div>
	....
</div>
```
這邊只要抓<div class="title">底下a的連結
```python
    response.css('div.title a')
```

### extract data 
<img src = "2.PNG"></img>

一樣在shell 底下
```
url = 'https://www.ptt.cc/bbs/Beauty/M.1587404155.A.04D.html'
cookies = {"over18": "1"}
response = scrapy.Request(url, cookies=cookies)
fetch(response)
```

由上圖可以發現只要抓<span clsss="article-meta-value">的值就可以把資訊抓起來
```python
>>> response.css("span.article-meta-value::text").extract()
['tibo96033 (鯉魚)', 'Beauty', '[正妹] 峮峮', 'Tue Apr 21 01:35:53 2020']
```    

get image url
```html
	<div id="main-content" class="bbs-screen bbs-content">
		<a href="https://i.imgur.com/jE9G3kv.jpg" target="_blank" rel="nofollow">https://i.imgur.com/jE9G3kv.jpg</a>
        <div class="richcontent">
            <blockquote class="imgur-embed-pub" lang="en" data-id="jE9G3kv">
                <a href="//imgur.com/jE9G3kv"></a>
            </blockquote>
            <script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
		</div>
        
		<a href="https://i.imgur.com/nudo8tI.jpg" target="_blank" rel="nofollow">https://i.imgur.com/nudo8tI.jpg</a>
			<div class="richcontent">
				<blockquote class="imgur-embed-pub" lang="en" data-id="nudo8tI">
                    <a href="//imgur.com/nudo8tI"></a>
				</blockquote>
				<script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>
			</div>
        .....
    </div>    
```
這邊我們抓div.richcontent blockquote.imgur-embed-pub 底下的連結

```python
>>> response.css("div.richcontent blockquote a::attr(href)").extract()
['//imgur.com/jE9G3kv', '//imgur.com/nudo8tI', '//imgur.com/I5Tsl2H', '//imgur.com/yeTwTLl', '//imgur.com/5dLWpUe', '//imgur.com/NjsHGMQ', '//imgur.com/jZqQT4A']
```

### DownLoad Image
在setting.py 設定 IMAGES_STORE = 'images'

pipelines.py 
```python
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import urllib.request

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_filename(path):
    return path.split('/')[-1]


class DownLoad(ImagesPipeline):
    def get_media_requests(self, item, info):
        save_path = "D:\\crawl\\{0}\\{1}\\".format(item['board'],item['title']) 
        create_folder(save_path)        

        for image_url in item['image_urls']:	
            urllib.request.urlretrieve(image_url,save_path + get_filename(image_url))
            
        
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]    
        if not image_paths:
            raise DropItem("Item contains no images")        
        return item	   

```

### spider
把上面測試的一一寫入
#### CrawlSpider

```python
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BeautyCrawlSpider(CrawlSpider):
    name = 'ptt_beauty'
    allowed_domains = ['ptt.cc']      
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.DownLoad': 800,}}    
    def start_requests(self):       
        url = 'https://www.ptt.cc/bbs/Beauty/index.html' 
        yield scrapy.Request(url, cookies ={'over18': '1'})    
       
    rules = ( 
        Rule(LinkExtractor(restrict_css ='a.wide ')),
        Rule(LinkExtractor(restrict_css='div.title a',restrict_text = r'\[正妹\].*'), callback ='parse_beauty'),
    )  
    
    def parse_beauty(self, response):          
        author,board,title,date_time = response.css("span.article-meta-value::text").extract()    
        image_urls = response.xpath('//div[contains(@class,"bbs-screen")]//a[contains(@href, ".jpg")]/@href').extract()
        yield {  
            'board':board,
            'title': title,    
            'link': response.url,
            'image_urls':image_urls
        }
```

#### Spider

```python
class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['ptt.cc']  
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.DownLoad': 800,}}    
    page = 0
    max_page = 2 
    
    def start_requests(self):  
        url = 'https://www.ptt.cc/bbs/Beauty/index.html' 
        yield scrapy.Request(url, cookies ={'over18': '1'},callback = self.parse)        

    def parse(self, response):    
        self.page += 1    
        
        for link in response.css('div.title a'):            
            if '[正妹]' in link.css('::text').get():                
                yield response.follow(link, callback = self.parse_article)          
        
        if self.page <= self.max_page:
            yield response.follow(response.css('a.wide')[1], self.parse)        
   

    def parse_article(self, response):        
        author,board,title,date_time = response.css("span.article-meta-value::text").extract()        
        content = response.css("#main-content::text").extract()
        img_urls = response.xpath('//div[contains(@class,"bbs-screen")]//a[contains(@href, ".jpg")]/@href').extract()
            
        item = {
            'board':board,
            'author': author,
            'title': title,
            'date_time': date_time,
            'content':content,
            'image_urls':img_urls,
        }
        yield item   
```       



  


















