import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BeautyCrawlSpider(CrawlSpider):
    name = 'ptt_beauty'
    allowed_domains = ['ptt.cc']      
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.PttImageDownLoad': 800,}}        
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

  
class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['ptt.cc']  
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.PttImageDownLoad': 800,}}        
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

            
from example.items import PttItem
class BeautySpiderItem(scrapy.Spider):
    name = 'beauty_item'
    allowed_domains = ['ptt.cc']  
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
        image_urls = response.xpath('//div[contains(@class,"bbs-screen")]//a[contains(@href, ".jpg")]/@href').extract()
        
        item = PttItem()        
        item['board'] = board
        item['author'] = author
        item['title'] = title
        item['date_time'] = date_time
        item['content'] = content
        item['image_urls'] = image_urls
        yield item   
      
            
            
            
            
            
            
            
            
            
            
            
            
            
            

        
        