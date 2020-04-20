# Two-direction Crawling

想要抓作者的相關資料,必須在每一頁裡面在連結到作者的資訊頁<br>
這算是Two-direction Crawling<br>

## Two-direction Crawling with Spider

```python 
class Two_direction_QuotesSpider(scrapy.Spider):
    name = 'author'
    start_urls = [
        'http://quotes.toscrape.com'] 


    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
```
parse　可以寫成這種方式
```python
    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)
```        

## CrawlSpider

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
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
```