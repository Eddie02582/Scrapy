# 雙向爬蟲

想要抓作者的相關資料,必須在每一頁裡面在連結到作者的資訊頁<br>

```python
class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for author_page_link in response.css('.author + a'):  
            yield response.follow(author_page_link, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            for pagination_link in response.css('li.next a'):
                yield response.follow(pagination_link, callback = self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get(),
            'birthdate': response.css('.author-born-date::text').get(),
            'bio': response.css('.author-description::text').get(),
        }
```

在cmd執行
```
    scrapy crawl author -o author.csv
```



使用到Scrapy 教學4]爬蟲撰寫介紹到的response.follow_all(anchors, callback=self.parse),簡化

```python
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

class AuthorCrawlSpider(CrawlSpider):
    name = 'author_crawl'
    start_urls = ['http://quotes.toscrape.com'] 

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