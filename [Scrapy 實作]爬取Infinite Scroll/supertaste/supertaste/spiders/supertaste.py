import scrapy
import json

class SupertasteSpider(scrapy.Spider):
    name = 'supertaste'
    def start_requests(self):       
        for page in range(1,66):
            url = "https://supertaste.tvbs.com.tw/review/LoadMoreOverview/%s" %page
            yield scrapy.Request(url)    

    def parse(self, response): 
        datas = json.loads(response.body.decode('utf-8'))
        # for data in datas:
            # url = data['url']
            # yield response.follow(url, callback = self.parse_detail)             
        
        detail_links = [data['url'] for data in datas]     
        yield from response.follow_all(detail_links, self.parse_detail)
        
        
    def get_array_data(self,array):      
        return array[0] if array else ""
    
    def parse_detail(self, response):  
        show_name = self.get_array_data(response.css('div.newsdetail_content div.title h1::text').re(r'.*?《(.*?)》'))          
        
        date =  self.get_array_data(response.css('div.icon_time::text').re(r'(\d+/\d+/\d+).*'))   
        if show_name:     
            for store in response.css('div.store_div'):
                image_url = store.css('img.lazyimage::attr(data-original)').get()
                name = store.css('div.store_info h2::text').get()           
                address = self.get_array_data(store.css('div.store_info p::text').re(r'地址：(.*)'))
                business_hours = self.get_array_data(store.css('div.store_info p::text').re(r'時間：(.*)'))
                telephone = self.get_array_data(store.css('div.store_info p::text').re(r'電話：(.*)'))  
                if '食尚玩家購物網' in name:
                    continue
                
                yield {                    
                    'date' : date,
                    'show_name' :  show_name,
                    'url':response.url,
                    'name' :  name,
                    'image_url' : image_url,
                    'address' : address,
                    'business_hours' :  business_hours,          
                    'telephone' :  telephone,
                    #'points' : points
                }
            


