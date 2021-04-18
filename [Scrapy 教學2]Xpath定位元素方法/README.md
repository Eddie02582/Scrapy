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
</div>```
 
 
## get tag elements 
取得div class="quote" 底下span class = "text"這個元素為例,xpath 

寫法為//div[contains(@class, "quote")]/span[contains(@class, "text")]<br>

這邊可以發現前面使用//而後面使用/,差別在於//不管前面的那層,/指的是絕對位置




```python
response.xpath('//div[contains(@class, "quote")]/span[contains(@class, "text")]')
>>>[<Selector xpath='//div[contains(@class, "quote")]/span[contains(@class, "text")]' data='<span class="text" itemprop="text">“T...'>,
```
注意這邊取得的是select,如果要取得元素可以透過get()或是getall()

### get string (extract_first() /get)

```python
>>> response.css('div.quote span.text').get()
'<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>'
```

### get list string (extract /getall)

取得所有元素getall()
```python
>>> response.css('div.quote span.text').getall()
['<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>',
'<span class="text" itemprop="text">“It is our choices, Harry, that show what we truly are, far more than our abilities.”</span>', 
'<span class="text" itemprop="text">“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”</span>',
'<span class="text" itemprop="text">“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”</span>',
'<span class="text" itemprop="text">“Imperfection is beauty, madness is genius and it\'s better to be absolutely ridiculous than absolutely boring.”</span>',
'<span class="text" itemprop="text">“Try not to become a man of success. Rather become a man of value.”</span>', 
'<span class="text" itemprop="text">“It is better to be hated for what you are than to be loved for what you are not.”</span>',
 '<span class="text" itemprop="text">“I have not failed. I\'ve just found 10,000 ways that won\'t work.”</span>',
 '<span class="text" itemprop="text">“A woman is like a tea bag; you never know how strong it is until it\'s in hot water.”</span>', '<span class="text" itemprop="text">“A day without sunshine is like, you know, night.”</span>'
 ]
```

## how to get element value

### get text
使用::text來取得

```
>>> response.css('div.quote span.text::text').get()
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
```

### 取得屬性
使用::attr(屬性)
這邊取得<a class="tag" 底下的href
```
>>> response.css('div.tags a.tag::attr(href)').get()
'/tag/change/page/1/'
```