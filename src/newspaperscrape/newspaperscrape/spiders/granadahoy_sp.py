
from gc import callbacks
from itertools import starmap
from re import T
from sqlite3 import Date
from urllib import response
from urllib.parse import urljoin
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from newspaperscrape.mybasespider import BaseSpider
from newspaperscrape.bow.bow import bagOfWords
from datetime import datetime

import os
from os import remove, path

class granadahoySpider(BaseSpider):

  # String which define the name for this spider
  name= "granadahoy"

  # List of URLs where the spider will begin to crawl from
  start_urls = [
      #'https://www.granadahoy.com',
      'https://www.granadahoy.com/granada/',
      'https://www.granadahoy.com/granada/?page=2',
      'https://www.granadahoy.com/granada/?page=3',
      'https://www.granadahoy.com/granada/?page=4',
      'https://www.granadahoy.com/granada/?page=5',
      'https://www.granadahoy.com/granada/?page=6'
    ]

  base_url = 'https://www.granadahoy.com'

  custom_settings = {
            'FEED_URI': '../files/json/gh_today.json',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'utf-8',
            'ROBOTSTXT_OBEY': False
    }
    
  

  # Extract links for the next url
  rules = [Rule(LinkExtractor(allow="https://www.granadahoy.com"), callback= "parse"
                    ),
          Rule(LinkExtractor(allow="https://www.granadahoy.com"), callback= "parse_nav")
                    ]

  

  # Default callback used by Scrapy to process downloaded responses (Dialy update of news, so it is only need to parse the main page)
  def parse(self, response):
    # Links located on the main page
    np_links = response.css('.gd .headline a::attr(href)').getall()
    np_links+= response.css('.mt .rel-content a::attr(href)').getall()

    for link in np_links: # Main page parsing
        yield response.follow(link, callback= self.parse_link, cb_kwargs={'url': response.urljoin(link)})
    
      
  # 
  # Comment if is only needed a daily update from the newspaper
  #
  # Default callback used by Scrapy to process downloaded responses
  """
  def parse(self, response):
     
    
      # Links located on the main page
      np_links = response.css('.gd .headline a::attr(href)').getall()
      np_links+= response.css('.mt .rel-content a::attr(href)').getall()

      # Links located on nav
      nav_links= response.xpath('//ul[contains(@class, "nav-join")]//li[@class="nav-item droptab"]//a/@href').getall()
      nav_links+= response.xpath('//ul[contains(@class, "nav-join")]//li[@class="nav-item"]//a/@href').getall()
        
      for link in np_links: # Main page parsing
        yield response.follow(link, callback= self.parse_link, cb_kwargs={'url': response.urljoin(link)})

      # Allowing only urls content on base_url
      for link in nav_links: # Nav parsing
        if self.base_url in response.urljoin(link):
          yield response.follow(link, callback= self.parse_nav, cb_kwargs={'url': response.urljoin(link)})
    """

  
  # Parsing of the nav
  def parse_nav(self, response, **kwargs):
      
      link= kwargs['url']
      section_links= response.xpath('//div[@class="gd"]//h2[contains(@class,"headline")]//@href').getall()

      for link in section_links:
        yield response.follow(link, callback= self.parse_link, cb_kwargs={'url': response.urljoin(link)})

      next_page= response.xpath('//div[contains(@class, "paginator")]//a[contains(@title, "Siguiente")]/@href').get()
      if next_page is not None:
        next_page= response.urljoin(next_page)
        yield response.follow(next_page, callback= self.parse_nav, cb_kwargs={'url': response.urljoin(next_page)})

# Parsing of a general article's page
  def parse_link(self, response, **kwargs):
        link= kwargs['url']

        title= response.css('.pg-head .pg-bkn-headline::text').get()  
        date= response.xpath('//div[@class="pg-body"]//section[@class="nws-data"]//time[@class="dateline"]//text()').get()
        img= response.xpath('//div[@class="pg-article details"]//div[@class="pg-media"]//figure[@class="image-holder"]//img/@src').get()
        img= response.urljoin(img)
        resume= response.xpath('//header[@class="pg-head"]//ul//li//p//text()').get()
        content= response.xpath('//div[@class="mce-body "]//p[contains(@class,"mce")]').getall()
        aux_content= "".join(content).strip()
        date_format= response.xpath('//head//meta[@property="article:published_time"]/@content').get()
        
        bow= bagOfWords()
        normalize_content = bow.normalizeText(aux_content)
        normalize_title= bow.normalizeText(title)
    
        if bow.findRegex(normalize_content):
            yield{
                'relevance': bow.relevance(normalize_content) + 10*bow.relevance(normalize_title),
                'np': "granadahoy",
                'url': link,
                'date': date,
                'date_format':date_format,
                'img': img,
                'title': title,
                'content': aux_content,
                'resume': resume,
            }