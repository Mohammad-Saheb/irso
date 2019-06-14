# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from .models import MusicDB,db_connect,create_table
import requests
import os
import telegram
import re
from subprocess import call
#from libs.tag import add_details,add_albumart
from .libs.tag import add_details,add_albumart

#class MyscPipeline(object):
    #def process_item(self, item, spider):
        #return item
#bot = telepot.Bot(token='354062396:AAGQWxaZWK9K7zBHKfyV-Jpx0rLOf2rIwc0')
bot = telegram.Bot(token='354062396:AAGQWxaZWK9K7zBHKfyV-Jpx0rLOf2rIwc0')
ad='@IranSong'


class MyscPipeline(object):


    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        musicdb = MusicDB()

        musicdb.src_url = item["src_url"]
        musicdb.song_full_name =item["song_full_name"]
        musicdb.artist_name = item["artist_name"]
        musicdb.song_name = item["song_name"]
        musicdb.hq_mp3_file = item["hq_mp3_file"]
        musicdb.hq_cover_file = item["hq_cover_file"]
        musicdb.lq_mp3_file = item["lq_mp3_file"]
        musicdb.lq_cover_file = item["lq_cover_file"]
        musicdb.play_count = item["play_count"]
        musicdb.download_count = item["download_count"]
        musicdb.like = item["like"]
        musicdb.dislike = item["dislike"]
        musicdb.source = item["source"]
        musicdb.lyrics=item["lyrics"]
        musicdb.rating=item["rating"]
        musicdb.album=item["album"]
        music=session.query(MusicDB).filter_by(song_full_name=item["song_full_name"]).first()
        # if music is not None: return
        #
        # save_cover_name=item["song_full_name"]+'(@IranSong)' + '.jpg'
        # save_song_name=re.sub(u'[\W_]+', u'_',item["song_full_name"])+'(@IranSong)' + '.mp3'
        # save_song_preview_name = re.sub(u'[\W_]+', u'_', item["song_full_name"]) + '(@IranSong)' + '.ogg'
        #
        # if not os.path.isfile(save_song_name):
        #
        #     with open(save_song_name,'wb') as song:
        #         response=requests.get(item["hq_mp3_file"])
        #         song.write(response.content)
        #
        #     #Add tags
        #     add_details(save_song_name,item['song_name']+'(@IranSong)',item['artist_name'],item['album'],item['lyrics'])
        #     add_albumart(item["lq_cover_file"],save_song_name)
        #
        # print('converting')
        # print(save_song_name)
        # convert_result=call(["ffmpeg", "-i", save_song_name, "-ss","00:00:35","-to","00:00:65", "-ac", "1", "-map", "0:a",
        #                        "-codec:a", "libopus", "-b:a", "128k", "-vbr", "off", "-ar", "24000",
        #                        save_song_preview_name, "-y"], stdout=open(os.devnull, 'wb'),
        #                       stderr=open(os.devnull, 'wb'), stdin=open(os.devnull, 'wb')
        #                       )
        # print(convert_result)
        #
        # v_caption= 'Artist : #' + re.sub(u'[\W_]+', u'_',item['artist_name']) + '\r\n' +\
        #            'Title : ' + item['song_name'] + '\r\n' +\
        #            'Plays : '+item['play_count']+'\r\n'+ad
        # v_hq_cover_file_id=bot.send_photo(chat_id='@music4likes',
        #                                   caption=v_caption,
        #                                   photo=item["hq_cover_file"])['photo'][2]['file_id']
        # v_song_preview=bot.send_voice(chat_id='@music4likes',
        #                               voice=open(save_song_preview_name, 'rb'),
        #                               duration=30, caption=ad)
        # v_hq_mp3_file_id=bot.sendAudio(chat_id='@music4likes', audio=open(save_song_name, 'rb'),
        #                                             performer=item['artist_name'] + '(@IranSong)',
        #                                             title=item['song_name'] + '(@IranSong)',
        #                                             caption=ad
        #                                             )['audio']['file_id']
        # print(v_hq_mp3_file_id)
        #
        # musicdb.hq_cover_file_id = v_hq_cover_file_id
        # musicdb.hq_mp3_file_id = v_hq_mp3_file_id
        #
        # try:
        #     session.add(musicdb)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        return item

