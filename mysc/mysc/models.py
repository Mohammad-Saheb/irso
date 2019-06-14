# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    #return create_engine(get_project_settings().get("CONNECTION_STRING"))
    return create_engine("sqlite:///data.db")

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class MusicDB(DeclarativeBase):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True)
    src_url=Column('src_url',String(500))
    song_full_name=Column('song_full_name',String(300))
    artist_name=Column('artist_name',String(300))
    song_name=Column('song_name',String(400))
    album=Column('album',String(300))
    hq_mp3_file=Column('hq_mp3_file',String(500))
    hq_mp3_file_id=Column('hq_mp3_file_id',String(500))

    hq_cover_file=Column('hq_cover_file',String(500))
    hq_cover_file_id=Column('hq_cover_file_id',String(500))

    lq_mp3_file=Column('lq_mp3_file',String(500))
    lq_mp3_file_id=Column('lq_mp3_file_id',String(500))

    lq_cover_file=Column('lq_cover_file',String(500))
    lq_cover_file_id=Column('lq_cover_file_id',String(500))

    play_count=Column('play_count',String(100))
    download_count=Column('download_count',Integer)
    like=Column('like',Integer)
    dislike=Column('dislike',Integer)
    rating=Column('rating',Integer)
    lyrics=Column('lyrics',String(5000))
    source=Column('source',String(100))




