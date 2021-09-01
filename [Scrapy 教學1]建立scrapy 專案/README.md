# [Scrapy 教學]建立scrapy 專案

## 安裝
```
pip install scrapy 
```
如果出現以下錯誤,請下執行python -m pip install --upgrade pip,更新pip version
```
If you did intend to build this package from source, try installing a Rust compiler from your system package manager and ensure it is on the PATH during installation. Alternatively, rustup (available at https://rustup.rs) is the recommended way to download and update the Rust compiler toolchain.

    This package requires Rust >=1.41.0.

    ----------------------------------------
Command "d:\python_venv\crawl\scripts\python.exe -u -c "import setuptools, tokenize;__file__='C:\\Users\\Eddie\\AppData\\Local\\Temp\\pip-install-z0pi6j9r\\cryptography\\setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" install --record C:\Users\Eddie\AppData\Local\Temp\pip-record-7y5uxmx3\install-record.txt --single-version-externally-managed --compile --install-headers d:\python_venv\crawl\include\site\python3.6\cryptography" failed with error code 1 in C:\Users\Eddie\AppData\Local\Temp\pip-install-z0pi6j9r\cryptography\
You are using pip version 18.1, however version 21.0.1 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.
```

## 建立案子
建立專案的指令如下
```
   scrapy startproject [name]
```
 
下scrapy startproject example,會吐出下列訊息

```
You can start your first spider with:
    cd example
    scrapy genspider example example.com
```

並且會產生如下
```
example/
    scrapy.cfg            # deploy configuration file

    example/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```            

## 建立爬蟲
爬蟲的指令
```
	scrapy genspider [name] [domain]
```
在cmd 下
```
	cd exmaple
	scrapy genspider quotes  quotes.toscrape.com
```
spiders資料夾就會產生quotes.py

<ul>
	<li>allowed_domains:允許網址的domain</li>
	<li>start_urls:要爬蟲的網址</li>
	<li>parse:用來解析網頁資料</li>
	<li>name:cmd 執行爬蟲的名字</li>
</ul>

```python 
import scrapy
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
```





 
 
 
 
 
 
 
 
 
 
 
 
 
 