# -*- coding: utf-8 -*-
import scrapy
from ..items import Bia2Item
import re
import json
import requests


class AloonakSpider(scrapy.Spider):
    name = 'rj'
    allowed_domains = ['radiojavan.com']
    start_urls = ['https://www.radiojavan.com/']

    def get_download_link(filename):
        response = requests.get("https://www.radiojavan.com/mp3s/mp3_host/?id=%s" %(file_name))
        url = str(json.loads(response.text)['host']) + "/media/mp3/" + file_name + ".mp3"
        return url

    def parse(self, response):
        download_pages =response.css('.grid')[2].css('a::attr(href)').extract()
        self.log(download_pages)

        for download_page in download_pages:
            new_url = 'https://www.radiojavan.com' + download_page        
            yield scrapy.Request(new_url, self.parse_download_page)
        
    def parse_download_page(self, response):
    
        item = Bia2Item()
        # todo:get from parse method
        item["src_url"] = response.css('div.fb-comments::attr(data-href)').extract_first().strip()
        item["song_full_name"]=response.css('div.fb-comments::attr(data-href)').extract_first().strip().split('/')[-1]
        item["artist_name"] = response.css('div.songInfo span.artist::text').extract_first().strip()
        item["song_name"] = response.css('div.songInfo span.song::text').extract_first().strip()
        try:
            item["producers"]=''.join(response.css('.mp3Description::text').extract()).strip().encode('utf8')
        except Exception as e:
            self.log(e)
            item["producers"] = ''
            pass
        
        filename=response.css('.rjform::attr(action)').extract_first().split('/')[3]
        host_response = requests.get("https://www.radiojavan.com/mp3s/mp3_host/?id=%s" %(filename))             
        item["hq_mp3_file"] = str(json.loads(host_response.text)['host']) + "/media/mp3/" + filename + ".mp3"
        
        item["hq_cover_file"] = response.css('.artwork img::attr(src)').extract_first().strip()
        item["lq_mp3_file"] = ''
        item["lq_cover_file"] = ''
        item["play_count"]=response.css('div.songInfo span.views::text').extract_first().strip().split()[1]
        item["download_count"]='0'
        item["like"]=response.css('#mp3_likes span.rating::text').extract_first().strip().split()[0]
        item["dislike"]=response.css('#mp3_dislikes span.rating::text').extract_first().strip().split()[0]
        try:
            lyrics=''
            for lyc in response.css('.lyricsFarsi::text').extract() :
                lyrics+=lyc.strip()+'\r\n'               
            item["lyrics"]=lyrics.encode('utf8')
            #''.join(response.css('.lyricsFarsi::text').extract()).strip().encode('utf8')
            #' '.join(response.css('.mohtava h3+p::text').extract()).strip().encode('utf8')
        except Exception as e:
            self.log(e)
            item["lyrics"]=''
            pass

        item["teaser"]=''
        item["insta_desc"]=''
        item["rating"]='0'
        item["album"]='Unknown'
        item["source"]='rj'

        return item
        # pass       