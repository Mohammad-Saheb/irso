# -*- coding: utf-8 -*-
import scrapy
from ..items import Bia2Item
import re

class AloonakSpider(scrapy.Spider):
    name = 'aloonak'
    allowed_domains = ['aloonak.com']
    start_urls = ['https://aloonak.com/category/post/lastupdate/']

    def parse(self, response):
        download_pages = response.css('.box a::attr(href)').extract()
        self.log(download_pages)

        for download_page in download_pages[:2]:
            yield scrapy.Request(download_page, self.parse_download_page)

    def parse_download_page(self, response):
        item = Bia2Item()
        # todo:get from parse method
        item["src_url"] = response.css('.scroll-bar a.relate-box-a::attr(href)').extract_first().strip()
        item["song_full_name"]=response.css('.scroll-bar a.relate-box-a::attr(title)').extract_first().strip()
        item["artist_name"] = response.css('p.singer-title a::text').extract_first().strip()
        item["song_name"] = response.css('p.track-title::text').extract_first().replace("-", "").strip()
        item["producers"]=re.sub('<br\s*?>', '\n', response.css('div.producers::text').extract_first()).strip()
        item["hq_mp3_file"] = response.css('a[field=link320]::attr(href)').extract_first().strip()
        item["hq_cover_file"] = response.css('img.post-thumbnail::attr(src)').extract_first().strip()
        item["lq_mp3_file"] = response.css('a[field=link128]::attr(href)').extract_first().strip()
        item["lq_cover_file"] = ''
        item["play_count"]=response.css('span[field=post_views]::text').extract_first().strip()
        item["download_count"]=0
        item["like"]=response.css('span[field=post_like]::text').extract_first().strip()
        item["dislike"]=0
        item["lyrics"]=re.sub('<br\s*?>', '\n', response.css('.lyric[field=lyrics]').extract_first()).strip()
        if item["lyrics"].find('There is no lyric yet') >0 : item["lyrics"]= ''
        item["rating"]=0
        item["album"]='Unknown'
        item["source"]='aloonak'

        return item
        # pass

