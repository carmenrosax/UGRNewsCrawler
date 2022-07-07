import scrapy
import os


class BaseSpider(scrapy.Spider):

    """custom_settings = {
        'FEED_URI': '../files/js/np.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }"""
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def parse(self, response):
        pass