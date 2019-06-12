# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin


class Bia2Spider(scrapy.Spider):
    name = 'bia2'
    allowed_domains = ['bia2.com']
    start_urls = ['https://www.bia2.com/music/latest.php']

    def parse(self, response):
        download_pages = response.css('a.music_player_page::attr(href)').extract()
        # self.log(download_pages)
        for download_page in download_pages[2:]:
            new_url = 'https://www.bia2.com' + download_page
            # self.log(new_url)
            yield scrapy.Request(new_url, self.parse_download_page)

    def parse_download_page(self, response):
        src_url = response.css('div.fb-comments::attr(data-href)').extract_first()
        artist_name = response.css('div.intro-holder a.artist_profile::text').extract_first()
        song_name = response.css('div.intro-holder h1::text').extract_first().replace("-", "").strip()
        hq_mp3_file = response.css('form[method]::attr(action)').extract_first()
        hq_cover_file = response.css('li.add_all_without_cover_ol::attr(cover_src)').extract_first()
        lq_mp3_file = response.css('li.add_all_without_cover_ol::attr(id)').extract_first()
        lq_cover_file = response.css('img.artist-round::attr(src)').extract_first()
        row_data = zip(src_url, artist_name, song_name, hq_mp3_file, hq_cover_file, lq_mp3_file, lq_cover_file)
        self.log(row_data)
        print(row_data)
        # pass
