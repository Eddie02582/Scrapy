import scrapy
from example.items import QuotesItem

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
    name = "quotes_item"   
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
  
   
   
class  QuotesLoginSpider(scrapy.Spider):
    name = "login" 
    
    def start_requests(self):         
        url = 'http://quotes.toscrape.com/login'
        yield scrapy.FormRequest(url,formdata={'username':'1234','password':'777'},callback = self.check_login)
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
    def check_login(self,response):
        if 'Logout' in response.text:
            print ('login sucess')
            yield scrapy.Request(response.url,callback = self.parse)
        else:
            print ('login fail')
  
class  QuotesLoginSpider(scrapy.Spider):
    name = "login2" 
    
    def start_requests(self):  
        return [
            scrapy.Request(
                'http://quotes.toscrape.com/login',
                callback=self.login)
        ]
    
    
    def login(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={"username": "1234", "password": "777"},            
        )
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

  
            
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
        
        
        
        
        
        