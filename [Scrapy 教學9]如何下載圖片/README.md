# How to Download Image

想要抓作者的相關資料,必須在每一頁裡面在連結到作者的資訊頁<br>
這算是Two-direction Crawling<br>

## Use default
在setting.py設定

```python 
    ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
    IMAGES_STORE = 'images
```

並在items.py 設定對應欄位,並新增image_urls(必要)

```
from scrapy.item import Item, Field
class PttItem(Item):
    board = Field()  
    author = Field()  
    title = Field()
    date_time = Field()    
    content = Field()
    image_urls = Field()

```
 
## User Define
通常需要自訂檔名和儲存路徑時使用,繼承ImagesPipeline並修改其內容

```python
def get_filename(path):
    return path.split('/')[-1]       

import scrapy
class ImageDownLoad(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:	          
            yield scrapy.Request(
              image_url,
              meta={
                'title': item['title'],
                'board': item['board'],
                'file_name': get_filename(image_url)
              }
            )

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    def file_path(self, request, response=None, info=None):
        file_name = request.meta['file_name']
        title = request.meta['title']
        board = request.meta['board']
        path = "D:\\crawl\\{0}\\{1}\\".format(board,title)
        return path + file_name
```  
     
並在spider.py 爬蟲設定新增
```python
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.ImageDownLoad': 800,}}   
```

```python
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class BeautyCrawlSpider(scrapy.Spider):
    name = 'name' 
    start_urls = [
        'http://quotes.toscrape.com/page/1/',        
    ]    
    custom_settings = {'ITEM_PIPELINES': {'example.pipelines.PttImageDownLoad': 800,}}   
    
    def parse(self, response):          
        pass
```




     