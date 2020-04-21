# -*- coding: utf-8 -*-
import scrapy
from example.items import QuotesItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # allowed_domains = ['example.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        
    ]   


    def parse(self, response):  
        for quote in response.css("div.quote"):  
            Item = QuotesItem()
            Item['text'] = quote.css("span.text::text").get(),
            Item['author'] = quote.css("small.author::text").get()
            Item['tags'] = quote.css("div.tags a.tag::text").extract()              
            yield Item
            
        next_page = response.css('li.next a::attr(href)').extract_first()   
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
       

            

class Two_direction_QuotesSpider(scrapy.Spider):
    name = 'author'
    start_urls = [
        'http://quotes.toscrape.com'] 


    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
        
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
class QuotesCrawlSpider(CrawlSpider):
    name = 'author2'
    start_urls = [
        'http://quotes.toscrape.com'] 

    rules = (
       
	    #next Page
        Rule(LinkExtractor(restrict_css ='li.next a')),
        #Page link
        Rule(LinkExtractor(restrict_css='.author + a'), callback ='parse_author'),
    )    

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

        
















      
        