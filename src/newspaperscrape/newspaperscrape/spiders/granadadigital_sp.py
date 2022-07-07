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
    name= "granadadigital"

    # List of URLs where the spider will begin to crawl from
    start_urls = [
        #'https://www.granadadigital.es/seccion/granada/',
        'https://www.granadadigital.es/?s=+',
        'https://www.granadadigital.es/page/2/?s=+',
        'https://www.granadadigital.es/page/3/?s=+',
        'https://www.granadadigital.es/page/4/?s=+',
        'https://www.granadadigital.es/page/5/?s=+'
    ]

    base_url = 'https://www.granadadigital.es'


    custom_settings = {
            'FEED_URI': '../files/json/gd_today.json',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'utf-8',
            'ROBOTSTXT_OBEY': False
    }
   
    def parse(self, response):
    
            # Extracting all links located on the main page
            links= response.xpath('//div//article//h2[@class="post-title"]//a/@href').getall()

            # Parsing of the extracted links
            for link in links: 
                yield response.follow(link, callback= self.parse_article, cb_kwargs={'url': response.urljoin(link)})
    
    # 
    # Comment if is only needed a daily update from the newspaper
    #
    # Default callback used by Scrapy to process downloaded responses
    """
    def parse(self, response):
    
            # Extracting all links located on the main page
            links= response.xpath('//div[@class="row content-news"]//h2[@class="post-title"]//a/@href').getall()

            # Parsing of the extracted links
            for link in links: 
                yield response.follow(link, callback= self.parse_article, cb_kwargs={'url': response.urljoin(link)})

            # Pagination
            urls=response.xpath('//ul[@class="pagination"]//a[contains(@class,"page-link")]/@href').getall()
            next_page= urls[-1]

            
            # recursive calling if a new page exists.
            next_page= response.urljoin(next_page)
            yield response.follow(next_page, callback= self.parse_following_page, cb_kwargs={'url': response.urljoin(next_page)})
    """
      
    def parse_following_page(self, response, **kwargs):
    
            link= kwargs['url']
           
            # Extracting all links located on the main page
            links= response.xpath('//h2[@class="post-title"]//a/@href').getall()

            # Parsing of the extracted links
            for link in links: 
                yield response.follow(link, callback= self.parse_article, cb_kwargs={'url': response.urljoin(link)})

            # Pagination
            pages= response.xpath('//ul[@class="pagination"]//a[contains(@class,"page-link")]//text()').getall()
            
            if pages[-1]!= 'Siguiente ':
                next_page= None
            else:
                urls=response.xpath('//ul[@class="pagination"]//a[contains(@class,"page-link")]/@href').getall()
                next_page= urls[-1]


            if next_page is None:
                yield{
                    'np': pages[-2],
                    'url': "No hay siguiente pagina",
                }
            else: # recursive calling if a new page exists.
               
                #next_page= response.urljoin(next_page)
                yield response.follow(next_page, callback= self.parse_following_page, cb_kwargs={'url': response.urljoin(next_page)})
        
    def parse_article(self, response, **kwargs):
        
        link= kwargs['url']
        title= response.xpath('//h1//text()').get()
        resume= response.xpath('//div[@class="single-new-content"]//p//text()').get()
        content= response.xpath('//div[@class="single-new-content"]//p').getall()
        img= response.xpath('//div[@class="single-new-img"]//img/@data-src').get()
        date= response.xpath('//span[@class="single-new-date"]//text()').get()
        date_format= response.xpath('//span[@class="single-new-date"]//time/@datetime').get()

        aux_content= "".join(content).strip()
        bow= bagOfWords()
        normalize_content = bow.normalizeText(aux_content)
        normalize_title= bow.normalizeText(title)
    
        if bow.findRegex(normalize_content):
            
            yield{
                'relevance': bow.relevance(normalize_content) + 10*bow.relevance(normalize_title),
                'np': "granadadigital",
                'url': link,
                'date': date,
                'date_format': date_format,
                'img': img,
                'title': title,
                'content': aux_content,
                'resume': resume
            }

  