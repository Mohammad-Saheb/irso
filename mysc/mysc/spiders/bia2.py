# -*- coding: utf-8 -*-
import scrapy


class Bia2Spider(scrapy.Spider):
    name = 'bia2'
    allowed_domains = ['bia2.com']
    start_urls = ['https://www.bia2.com/music/latest.php']

    def parse(self, response):
        img = response.css('form').attib['action']
        yield img
