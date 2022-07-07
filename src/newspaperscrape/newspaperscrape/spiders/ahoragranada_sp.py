from gc import callbacks
from itertools import starmap
from urllib import response
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from datetime import datetime

from newspaperscrape.mybasespider import BaseSpider
import os
from newspaperscrape.bow.bow import bagOfWords

class ahoragranandaSpider(BaseSpider):

    # String which define the name for this spider
    name= "ahoragranada"

    # List of URLs where the spider will begin to crawl from
    start_urls = [
        'https://www.ahoragranada.com'
        ]

    base_url = 'https://www.ahoragranada.com'


    custom_settings = {
            'FEED_URI': '../files/json/ag_today.json',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'utf-8',
            'ROBOTSTXT_OBEY': False
    }
  
    # Default callback used by Scrapy to process downloaded responses (Dialy update)
    def parse(self, response):

         # Links located on the main page
        for article in response.selector.xpath('//div[@class="fw"]//div//article'):
            link= article.xpath('.//h3//a/@href').get()
            img= article.xpath('.//figure//img/@src').get()
            yield response.follow(link, callback= self.parse_article, cb_kwargs={'url': response.urljoin(link), 'img':response.urljoin(img)})
          
    

    # 
    # Comment if is only needed a daily update from the newspaper
    #    
    # Default callback used by Scrapy to process downloaded responses
    """def parse(self, response):

        for article in response.selector.xpath('//div[@class="w66 pr7 left loop col1"]//article[contains(@class,"noticia")]'):
            link= article.xpath('.//h3//a/@href').get()
            img= article.xpath('.//figure//img/@src').get()
            yield response.follow(link, callback= self.parse_article, cb_kwargs={'url': response.urljoin(link), 'img':response.urljoin(img)})
          
       
        next_page= response.xpath('//div[@class="fw pagination"]//a[@class="next page-numbers"]/@href').get()
        if next_page is not None:
            next_page= response.urljoin(next_page)
            yield response.follow(next_page, callback= self.parse)"""

     
    def parse_article(self, response, **kwargs):
        
        link= kwargs['url']
        img=kwargs['img']

        title= response.xpath('//h1//text()').get()
        date= response.xpath('//section[@class="fw"]//span[@class="date updated"]//text()').get()
        resume= response.xpath('//p[@class="intro"]//text()').get()
        content= response.xpath('//div[@class="w66 pr7 left col1"]//article[contains(@class,"fw main hentry ")]//p').getall()
        aux_content= "".join(content).strip()
        date_format= response.xpath('//head//meta[@property="article:published_time"]/@content').get()
       
 
        bow= bagOfWords()
        normalize_content = bow.normalizeText(aux_content)
        normalize_title= bow.normalizeText(title)
    
        if bow.findRegex(normalize_content):
            yield{
                'relevance': bow.relevance(normalize_content) + 5*bow.relevance(normalize_title),
                'np': "ahoragranada",
                'url': link,
                'date': date,
                'date_format': date_format,
                'img': img,
                'title': title,
                'content': aux_content,
                'resume': resume,
            }   

    
        