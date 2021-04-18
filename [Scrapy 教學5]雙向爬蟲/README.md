# 雙向爬蟲

想要抓作者的相關資料,必須在每一頁裡面在連結到作者的資訊頁<br>


就需要2個parse　函數,一個用來取得作者連結,另一個從作者連結取得資料
這邊使用到Scrapy 教學4]爬蟲撰寫介紹到的response.follow_all(anchors, callback=self.parse),將所有連結

```python 
    def parse(self, response):	
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)
```
解析作者連結資料
```python
    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get(),
            'birthdate': response.css('.author-born-date::text').get(),
            'bio': response.css('.author-description::text').get(),
        }
```

最後再使用一個response.follow_all將next的連結在疊加

```
class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)
		
        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get(),
            'birthdate': response.css('.author-born-date::text').get(),
            'bio': response.css('.author-description::text').get(),
        }
```


使用CrawlSpider

```python 
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
class QuotesCrawlSpider(CrawlSpider):
    name = 'author2'
    start_urls = [
        'http://quotes.toscrape.com'] 

    rules = (       
	    #next Page
        Rule(LinkExtractor(restrict_css ='li.next a')),
        #Page link
        Rule(LinkExtractor(restrict_css='.author + a'), callback ='parse_author'),
    )    

    def parse_author(self, response):    
        yield {
            'name': response.css('h3.author-title::text').get(),
            'birthdate': response.css('.author-born-date::text').get(),
            'bio': response.css('.author-description::text').get(),
        }
```