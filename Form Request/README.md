# Form Request

透過form request 傳送,formdata傳送資料,key 為element name


```python 
import scrapy
class  QuotesLoginSpider(scrapy.Spider):
    name = "login"
   
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]
    
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
            
```
