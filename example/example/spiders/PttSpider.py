import scrapy
from example.items import PttItem


class PTT_spider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']   
    page = 0
    max_page = 3
    def start_requests(self):        
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = 'https://www.ptt.cc/bbs/%s/index.html' %tag
            yield scrapy.Request(url, cookies ={'over18': '1'},callback = self.parse)    
    

    def parse(self, response):
    
        self.page += 1    
        # follow links to article pages
        yield from response.follow_all(css = 'div.title a', callback = self.parse_article)               
        if self.page <= self.max_page:
            yield response.follow(response.css('a.wide')[1], self.parse)        
   

    def parse_article(self, response):
        print (response.url)
        author,name,title,date_time = response.css("span.article-meta-value::text").extract()
        content = response.css("#main-content::text").extract()

        yield {
            'author': author,
            'title': title,
            'date_time': date_time,
            'content':content,
        }
       
class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['ptt.cc']  
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.DownLoad': 800,}}    
    page = 0
    max_page = 3
 
    
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
            # item = PttItem()  
            # item['board'] = board
            # item['author'] = author
            # item['title'] = title
            # item['date_time'] = date_time
            # item['content'] = content
            # item['image_urls'] = img_urls
            # yield item        
        
        

        
        
        
        
        
        
        