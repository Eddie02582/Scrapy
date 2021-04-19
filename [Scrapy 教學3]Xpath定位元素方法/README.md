# [Scrapy 教學]Xpath定位元素方法

在[Scrapy 教學]建立scrapy 專案,我們建立了專案,這篇介紹如何透過Xpath 定位來解析網頁<br>

這篇以官網範例的<a href ="https://quotes.toscrape.com/page/1/">網址</a>為例<br>

 
使用scrapy shell 來學習或測試,指令為
```
   scrapy shell url
```
從文章按右鍵,選擇檢查,可以看到網頁原始碼<br>　
觀察網頁原始碼觀察,每個block 都被div class="quote"包住
```html
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```
 
 
## Get tag elements 
取得div class="quote" 底下span class = "text"這個元素為例,xpath寫法如下
```
//div[contains(@class, "quote")]/span[contains(@class, "text")]
```
這邊可以發現前面使用//而後面使用/,差別在於//不管前面的那層,/指的是絕對位置



```python
response.xpath('//div[contains(@class, "quote")]/span[contains(@class, "text")]')
>>>[<Selector xpath='//div[contains(@class, "quote")]/span[contains(@class, "text")]' data='<span class="text" itemprop="text">“T...'>,
```


## How to get element value

### get text
使用/text()來取得

```python
>>> response.xpath('//div[contains(@class, "quote")]/span[contains(@class, "text")]/text()').get()
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
```

### 取得屬性
使用/@attr
```python
>>> response.xpath('//div[contains(@class, "tags")]/a/@href').get()
'/tag/change/page/1/'
```