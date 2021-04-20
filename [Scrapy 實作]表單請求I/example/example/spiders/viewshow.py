import scrapy
from scrapy_splash import SplashRequest,SplashFormRequest

class ViewshowSpider(scrapy.Spider):
    name = 'viewshow'
    allowed_domains = ['www.vscinemas.com.tw/']
  

    def start_requests(self):    
        url = 'https://www.vscinemas.com.tw/ShowTimes//ShowTimes/GetShowTimes'  
        yield scrapy.FormRequest(url,self.parse,formdata={'CinemaCode':'TP'})
        
    
    def parse(self, response):
        for section in response.xpath('body/div[contains(@class, "col-xs-12")]'):
            name = section.css('strong.MovieName::text').get()            
            dates = section.xpath('div[contains(@class,col-xs-12)]/strong[contains(@class, "LangEN")]/text()').re(r'\d+/\d+ [a-zA-Z]{3}')
                       
            times = []           
            info = {}
            for sessionTimeInfo in section.css('div.col-xs-12 div.SessionTimeInfo'):                
                times.append(":".join(sessionTimeInfo.css('div::text').re(r'\d+:\d+')))
            
            for date,time in zip(dates,times):
                info[date] = time
        
            yield {
                    'name': name,
                    'info':info    
            }





