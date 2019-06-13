# -*- coding: utf-8 -*-
#https://github.com/kalbhor/MusicNow

from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
#from urllib.request import urlopen
from urllib2 import urlopen

def add_details(file_name, title, artist, album, lyrics=""):

    tags = EasyMP3(file_name)
    tags["title"] = title
    tags["artist"] = artist
    tags["album"] = album
    tags.save()

    tags = ID3(file_name)
    uslt_output = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
    tags["USLT::'eng'"] = uslt_output

    tags.save(file_name)


def add_albumart(albumart, song_title):

    try:
        img = urlopen(albumart)  # Gets album art from url

    except Exception:
        #log.log_error("* Could not add album art", indented=True)
        return None

    audio = EasyMP3(song_title, ID3=ID3)
    try:
        audio.add_tags()
    except _util.error:
        pass

    audio.tags.add(
        APIC(
            encoding=3,  # UTF-8
            mime='image/png',
            type=3,  # 3 is for album art
            desc='Cover',
            data=img.read()  # Reads and adds album art
        )
    )
    audio.save()
