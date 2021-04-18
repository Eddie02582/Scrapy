# Form Request


介紹透過form request登入網頁,formdata為傳送資料,key 為element name

## FormRequest
```python 
import scrapy
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
            
```

## FormRequest.from_response
如果有hidden的欄位可以使用這個


```python 
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
```
           