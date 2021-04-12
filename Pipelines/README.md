# Pipelines
pipelines 主要處理輸出格式,有兩種處理方法
<ul>
    <li>處理大部分爬蟲時,在setting.py新增ITEM_PIPELINES </li>
    <li>對特定的爬蟲處裡,在spider.py 該爬蟲類別設定custom_settings</li>    
</ul>    



## Example1

假設我們有一個包含多個spider的應用，用來抓取日期。數據庫需要datetiem 格式。我們不想修改爬蟲，因為有很多都需要用<br>
在setting.py新增
```
    ITEM_PIPELINES = {'example.pipelines.tidyup.TidyUp': 100 }
```

pipelines.py
```python
class TidyUpPipeline:
    def process_item(self, item, spider):
        item['date'] = map(datetime.isoformat, item['date'])
        return item		
```
## Example Downdload Image


### use 內建
在setting.py 
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
IMAGES_STORE = 'images'


### User Define
spider.py 使用方法
新增 custom_settings = {'ITEM_PIPELINES': {'example.pipelines.PttImageDownLoad': 800,}}

```
def get_filename(path):
    return path.split('/')[-1]
       

import scrapy
class PttImageDownLoad(ImagesPipeline):
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














