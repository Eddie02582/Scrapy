import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }



        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)


class QuotesSpiderItems(scrapy.Spider):
    name = "quotes_items"
    custom_settings = {'ITEM_PIPELINES': {'example.JsonWriterPipeline': 800,}}  
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]
    
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            Item = QuotesItem()
            Item['text'] = quote.css("span.text::text").get(),
            Item['author'] = quote.css("small.author::text").get()
            Item['tags'] = quote.css("div.tags a.tag::text").extract()              
            yield Item
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)
            

from scrapy_splash import SplashRequest
class QuotesJsSpider(scrapy.Spider):
    name = "quotesjs"   

    def start_requests(self):     
        url = 'http://quotes.toscrape.com/js/'
        yield SplashRequest(url, self.parse, args={'wait': 0.5})
                
    
    def parse(self, response):        
        print (response.text)
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



            
            
class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()        
        
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }


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
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
        
        
        
        
        
        