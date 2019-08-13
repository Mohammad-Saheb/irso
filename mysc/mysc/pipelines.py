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
import urllib
import os

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
        engine.raw_connection().connection.text_factory = str
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        musicdb = MusicDB()

        musicdb.src_url = item["src_url"]
        musicdb.song_full_name =re.sub(u'[\W_]+', u'_',item["song_full_name"])
        musicdb.artist_name = item["artist_name"]
        musicdb.song_name = item["song_name"]
        #musicdb.hq_mp3_file = urllib.quote(item["hq_mp3_file"])
        musicdb.hq_mp3_file = item["hq_mp3_file"]
        musicdb.hq_cover_file = item["hq_cover_file"]
        musicdb.lq_mp3_file = item["lq_mp3_file"]
        musicdb.lq_cover_file = item["lq_cover_file"]
        musicdb.play_count = item["play_count"]
        musicdb.download_count = item["download_count"]
        musicdb.like = item["like"]
        musicdb.dislike = item["dislike"]
        musicdb.source = item["source"]
        musicdb.lyrics=item["lyrics"].decode('utf8')
        musicdb.rating=item["rating"]
        musicdb.album=item["album"]
        musicdb.insta_desc=item["insta_desc"].decode('utf8')
        musicdb.teaser=urllib.quote_plus(item["teaser"])
        musicdb.producers=item["producers"]
       
        #print(musicdb.lq_mp3_file)
        #if len(musicdb.hq_mp3_file) == 0 : return
        music=session.query(MusicDB).filter_by(src_url=item["src_url"]).first()
        if music is not None: return
               
        save_cover_name=musicdb.song_full_name+'(@IranSong)' + '.jpg'
        save_song_name=musicdb.song_full_name+'(@IranSong)' + '.mp3'
        save_song_preview_name = musicdb.song_full_name + '(@IranSong)' + '.ogg'

        if not os.path.isfile(save_song_name):

            try:
                print(musicdb.hq_mp3_file)
                with open(save_song_name,'wb') as song:
                    response=requests.get(musicdb.hq_mp3_file)
                    song.write(response.content)
            except Exception as e:
                print(e)
                pass

            try:            
                #Add tags
                add_details(save_song_name,item['song_name']+'(@IranSong)',item['artist_name'],item['album'],'@IranSong')#item['lyrics'])
                add_albumart(item["lq_cover_file"],save_song_name)
            except Exception as e:
                print(e)
                pass
                

        print('converting')
        #print(save_song_name)
        #print(save_song_preview_name)
        #todo:Check save_song_name length 
        try:    
            convert_result=call(["ffmpeg", "-i", save_song_name, "-ss","00:00:35","-to","00:01:05", "-ac", "1", "-map", "0:a",
                               "-codec:a", "libopus", "-b:a", "128k", "-vbr", "off", "-ar", "24000",
                               save_song_preview_name, "-y"], stdout=open(os.devnull, 'wb'),
                              stderr=open(os.devnull, 'wb'), stdin=open(os.devnull, 'wb')
                              )
            print(convert_result)
            print(save_song_name +'---'+save_song_preview_name)
            if(convert_result != 0) : return
        
            bot.send_message(chat_id='-1001401740901', text=item['src_url']+'\r\n'+'play_count : '   + item['play_count']+''+'\r\n'+'Source : ' + item['source']+'\r\n')
        
            v_caption= 'Artist : #' + re.sub(u'[\W_]+', u'_',item['artist_name']) + '\r\n' +\
                   'Title : '  + item['song_name'] + '\r\n' +\
                   'Plays : '  + item['play_count']+'\r\n'+\
                   'Full Name : #'  + musicdb.song_full_name+'\r\n'+ad
        
            v_hq_cover_file_id=''
            tmp_hq_cover_file=bot.send_photo(chat_id='-1001401740901',caption=v_caption,photo=musicdb.hq_cover_file)
            try:
                v_hq_cover_file_id=tmp_hq_cover_file['photo'][1]['file_id']
            except Exception as e:
                bot.send_message(chat_id='-1001401740901', text=str(tmp_hq_cover_file)+'\r\n'+'#'+musicdb.song_full_name)
                pass

            
            v_song_preview=bot.send_voice(chat_id='-1001401740901',
                                      voice=open(save_song_preview_name, 'rb'),
                                      duration=30, caption='#'+musicdb.song_full_name+'\r\n'+ad)
            v_hq_mp3_file_id=bot.sendAudio(chat_id='-1001401740901', audio=open(save_song_name, 'rb'),
                                                    performer=item['artist_name'] + '(@IranSong)',
                                                    title=item['song_name'] + '(@IranSong)',
                                                    caption='#'+musicdb.song_full_name+'\r\n'+ad
                                                    )['audio']['file_id']
                                                    
            #todo split lyrics
            if len(item['lyrics']) > 20 :
                bot.send_message(chat_id='-1001401740901', text='Lyrics : '+'\r\n'+item['lyrics'].decode('utf8')+'\r\n'+'#'+musicdb.song_full_name+'\r\n'+ad)
            
            if len(item['insta_desc']) > 0 :
                bot.send_message(chat_id='-1001401740901', text='Instagram : '+'\r\n'+item['insta_desc'].decode('utf8')+'\r\n'+item['teaser']+'#'+musicdb.song_full_name+'\r\n'+ad)
            
            if len(item['producers']) > 0 :
                bot.send_message(chat_id='-1001401740901', text='Producers : '+'\r\n'+item['producers'].decode('utf8')+'\r\n'+'#'+musicdb.song_full_name+'\r\n'+ad)


            print(v_hq_mp3_file_id)

            musicdb.hq_cover_file_id = v_hq_cover_file_id
            musicdb.hq_mp3_file_id = v_hq_mp3_file_id

            session.add(musicdb)
            session.commit()
        except Exception as e:
            session.rollback()
            
            #session.delete(musicdb)
            musicdb1 = MusicDB()
            musicdb1.src_url = item["src_url"]
            session.add(musicdb1)
            session.commit()
            print(e)
            bot.send_message(chat_id='-1001401740901', text=str(e)+'\r\n'+'Source : ' + item['source']+'\r\n'+'#'+musicdb.song_full_name)
            pass#raise
        finally:
            session.close()
        
        os.remove(save_song_name)
        os.remove(save_song_preview_name)
        return item

