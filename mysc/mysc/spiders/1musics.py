# -*- coding: utf-8 -*-
import scrapy
from ..items import Bia2Item
import re

class AloonakSpider(scrapy.Spider):
    name = '1musics'
    allowed_domains = ['1musics.com']
    start_urls = ['http://1musics.com/music/']

    def parse(self, response):
        download_pages = response.css('.head-post h2 a::attr(href)').extract()
        self.log(download_pages)

        for download_page in download_pages:
            yield scrapy.Request(download_page, self.parse_download_page)

    def parse_download_page(self, response):
        item = Bia2Item()
        # todo:get from parse method
        item["src_url"] = response.css('link[rel=canonical]::attr(href)').extract_first().strip()
        item["song_full_name"]=response.css('link[rel=canonical]::attr(href)').extract_first().split('/')[-2].strip()
        item["artist_name"] = response.xpath("//p[contains(text(), 'Download New Music')]/strong[1]/text()").extract_first().strip()
        item["song_name"] = response.xpath("//p[contains(text(), 'Download New Music')]/strong[2]/text()").extract_first().strip()
        try:
            item["producers"]=response.xpath("//span[contains(@style, '3366ff')]/text()").extract_first().strip().encode('utf8')
        except Exception as e:
            self.log(e)
            item["producers"] = ''
            pass
        item["hq_mp3_file"] = response.css('.mydlbox a::attr(href)')[1].extract().strip()
        item["hq_cover_file"] = response.css('.mohtava p img.size-full::attr(src)').extract_first().strip()
        item["lq_mp3_file"] = response.css('.mydlbox a::attr(href)')[0].extract().strip()
        item["lq_cover_file"] = ''
        item["play_count"]='0'
        item["download_count"]='0'
        item["like"]='0'
        item["dislike"]='0'
        try:
            item["lyrics"]=' '.join(response.xpath(u"//div/p[preceding-sibling::h3[contains(text(), 'متن')] and following-sibling::h2]/text()").extract()).encode('utf8')
            #' '.join(response.css('.mohtava h3+p::text').extract()).strip().encode('utf8')
        except Exception as e:
            self.log(e)
            item["lyrics"]=''
            pass
        try:
            item["teaser"]=response.css('.mohtava source::attr(src)').extract().strip()
        except Exception as e:
            self.log(e)
            item["teaser"]=''
            pass
        try:
            item["insta_desc"]=' '.join(response.xpath(u"//div//*[preceding-sibling::p[contains(text(),'توضیحات')] and following-sibling::p[contains(text(), 'تیزر')]]").css('*::text').extract()).encode('utf8')
            #' '.join(response.css('.mohtava').xpath('//h2/following-sibling::p/text()').extract()).strip().encode('utf8')
        except Exception as e:
            self.log(e)
            item["insta_desc"]=''
            pass            
        item["rating"]='0'
        item["album"]='Unknown'
        item["source"]='1musics'

        return item
        # pass