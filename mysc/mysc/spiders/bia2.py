# -*- coding: utf-8 -*-
import scrapy
#from urllib.parse import urljoin
from ..items import Bia2Item

class Bia2Spider(scrapy.Spider):
    name = 'bia2'
    allowed_domains = ['www.bia2.com']
    start_urls = ['https://www.bia2.com/music/latest.php']

    def parse(self, response):
        download_pages = response.css('a.music_player_page::attr(href)').extract()
        # self.log(download_pages)
        for download_page in download_pages:
            new_url = 'https://www.bia2.com' + download_page
            # self.log(new_url)
            yield scrapy.Request(new_url, self.parse_download_page)

    def parse_download_page(self, response):
        item = Bia2Item()
        item["src_url"] = response.css('div.fb-comments::attr(data-href)').extract_first().strip()
        item["song_full_name"]=response.css('div.item-holder a.title-song::text').extract_first().strip()
        item["artist_name"] = response.css('div.intro-holder a.artist_profile::text').extract_first().strip()
        item["song_name"] = response.css('div.intro-holder h1::text').extract_first().replace("-", "").strip()
        item["hq_mp3_file"] = response.css('form[method]::attr(action)').extract_first().strip()
        item["hq_cover_file"] = response.css('li.add_all_without_cover_ol::attr(cover_src)').extract_first().strip()
        item["lq_mp3_file"] = response.css('li.add_all_without_cover_ol::attr(id)').extract_first().strip()
        item["lq_cover_file"] = response.css('img.artist-round::attr(src)').extract_first().strip()
        item["play_count"]=response.css('#tab1 div div::text').extract_first().strip().split()[0]
        item["download_count"]='0'
        item["like"]='0'
        item["dislike"]='0'
        item["lyrics"]=''
        item["rating"]='0'
        item["album"]='Unknown'
        item["source"]='bia2'
        item["producers"]=''
        item["teaser"]=''
        item["insta_desc"]=''        

        return item
        # pass
