import scrapy

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BeautyCrawlSpider(CrawlSpider):
    name = 'ptt_beauty'
    allowed_domains = ['ptt.cc']  
    #custom_settings = {'ITEM_PIPELINES': {'example.pipelines.DownLoad': 1000,}}   
    
    def start_requests(self):       
        url = 'https://www.ptt.cc/bbs/Beauty/index.html' 
        yield scrapy.Request(url, cookies ={'over18': '1'})    
       
    rules = (       
	    #next Page
        #response.css('a.wide::attr(href)')[1]
        Rule(LinkExtractor(restrict_css ='a.wide ')),
        #Page link
        Rule(LinkExtractor(restrict_css='div.title a'), callback ='parse_beauty'),
    )  
    
    def parse_beauty(self, response):  
        
        author,board,title,date_time = response.css("span.article-meta-value::text").extract()    
        yield {  
            'board':board,
            'title': title,    
            'link': response.url,
            'images_url':response.css("blockquote a::attr(href)").extract()
        }
          
        
  
class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['ptt.cc']  
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.DownLoad': 800,}}    
    page = 0
    max_page = 1 
    
    def start_requests(self):  
        url = 'https://www.ptt.cc/bbs/Beauty/index.html' 
        yield scrapy.Request(url, cookies ={'over18': '1'},callback = self.parse)        

    def parse(self, response):
    
        self.page += 1    
        # follow links to article pages
        yield from response.follow_all(css = 'div.title a', callback = self.parse_article)   
        
        if self.page <= self.max_page:
            yield response.follow(response.css('a.wide')[1], self.parse)        
   

    def parse_article(self, response):        
        author,board,title,date_time = response.css("span.article-meta-value::text").extract()
        content = response.css("#main-content::text").extract()
        img_urls = response.xpath('//a[contains(@href, "imgur.com")]/@href').extract()
        if img_urls:
            img_urls = [url for url in img_urls if url.endswith('.jpg')]	            
            
            item = {
                'board':board,
                'author': author,
                'title': title,
                'date_time': date_time,
                'content':content,
                'image_urls':img_urls,
            }
            yield item   

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

        
        