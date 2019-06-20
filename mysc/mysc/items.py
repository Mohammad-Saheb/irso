# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Bia2Item(scrapy.Item):
    src_url=scrapy.Field()
    song_full_name=scrapy.Field()
    artist_name=scrapy.Field()
    song_name=scrapy.Field()
    album=scrapy.Field()
    hq_mp3_file=scrapy.Field()
    hq_mp3_file_id=scrapy.Field()

    hq_cover_file=scrapy.Field()
    hq_cover_file_id=scrapy.Field()

    lq_mp3_file=scrapy.Field()
    lq_mp3_file_id=scrapy.Field()

    lq_cover_file=scrapy.Field()
    lq_cover_file_id=scrapy.Field()

    play_count=scrapy.Field()
    download_count=scrapy.Field()
    like=scrapy.Field()
    dislike=scrapy.Field()
    lyrics=scrapy.Field()
    rating =scrapy.Field()
    source=scrapy.Field()

    producers=scrapy.Field()

    insta_desc=scrapy.Field()
    teaser=scrapy.Field()
	