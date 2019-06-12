# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import re


class RjSpider(scrapy.Spider):
    name = 'rj'
    allowed_domains = ['radiojavan.com']
    start_urls = ['http://radiojavan.com/']

    def parse(self, response):
        self.log(get_download_link('https://www.radiojavan.com/mp3s/mp3/The-Don-Nassim-AFX-Beraghs-Ba-Man?start=13761&index=1'))
        #pass


def get_download_link(link):
    media_type = re.split(r'/', link)[3]
    file_name = re.split(r'/', link)[5]

    session = requests.Session()
    if media_type == "podcasts":
        response = session.get("https://www.radiojavan.com/podcasts/podcast_host/?id=%s" %(file_name))
        url = str(json.loads(response.text)['host']) + "/media/podcast/mp3-256/" + file_name + ".mp3"
    elif media_type == "mp3s":
        response = session.get("https://www.radiojavan.com/mp3s/mp3_host/?id=%s" %(file_name))
        url = str(json.loads(response.text)['host']) + "/media/mp3/" + file_name + ".mp3"

    return url


