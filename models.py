from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, INTEGER, FLOAT, DATE, DATETIME, TINYINT, TIMESTAMP
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, joinedload


db = SQLAlchemy()

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, TIMESTAMP, Float, func
from sqlalchemy.dialects.mysql import VARCHAR, TINYINT
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = 'channel'

    channel_id = db.Column(VARCHAR(24), primary_key=True, nullable=False)
    channel_name = db.Column(Text, nullable=True)
    channel_url = db.Column(Text, nullable=True)
    channel_follower_count = db.Column(Integer, nullable=True)
    uploader = db.Column(Text, nullable=True)
    uploader_id = db.Column(Text, nullable=True)
    uploader_url = db.Column(Text, nullable=True)
    date_added = db.Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=True)
    last_updated = db.Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True
    )

    videos = relationship('Video', back_populates='channel', lazy="joined")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Format(db.Model):
    __tablename__ = 'format'

    format_id = db.Column(VARCHAR(16), nullable=True)
    format = db.Column(VARCHAR(50), primary_key=True, nullable=False)
    format_note = db.Column(VARCHAR(50), nullable=True)
    ext = db.Column(VARCHAR(16), nullable=True)
    resolution = db.Column(VARCHAR(20), nullable=True)
    width = db.Column(Integer, nullable=True)
    height = db.Column(Integer, nullable=True)
    fps = db.Column(Float, nullable=True)
    vcodec = db.Column(VARCHAR(16), nullable=True)
    acodec = db.Column(VARCHAR(16), nullable=True)
    protocol = db.Column(VARCHAR(50), nullable=True)
    dynamic_range = db.Column(VARCHAR(16), nullable=True)
    quality = db.Column(Integer, nullable=True)
    created_at = db.Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    last_updated = db.Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )

    video_formats = relationship('VideoFormat', back_populates='format_rel', lazy="joined")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(VARCHAR(11), primary_key=True, nullable=False)
    title = db.Column(Text, nullable=True)
    description = db.Column(Text, nullable=True)
    channel_id = db.Column(VARCHAR(24), ForeignKey('channel.channel_id', ondelete='SET NULL', onupdate='CASCADE'), nullable=True)
    channel_name = db.Column(Text, nullable=True)
    view_count = db.Column(Integer, nullable=True)
    like_count = db.Column(Integer, nullable=True)
    age_limit = db.Column(Integer, nullable=True)
    upload_date = db.Column(Date, nullable=True)
    release_date = db.Column(Date, nullable=True)
    release_year = db.Column(Integer, nullable=True)
    timestamp = db.Column(DateTime, nullable=True)
    release_timestamp = db.Column(DateTime, nullable=True)
    webpage_url = db.Column(Text, nullable=True)
    live_status = db.Column(VARCHAR(50), nullable=True)
    media_type = db.Column(VARCHAR(50), nullable=True)
    is_live = db.Column(TINYINT(1), nullable=True)
    was_live = db.Column(TINYINT(1), nullable=True)
    availability = db.Column(VARCHAR(50), nullable=True)
    publicly_available = db.Column(TINYINT(1), nullable=True)
    created_at = db.Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    last_updated = db.Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )

    channel = relationship('Channel', back_populates='videos', lazy="joined")
    thumbnails = relationship('Thumbnail', back_populates='video', lazy="joined")
    video_formats = relationship('VideoFormat', back_populates='video', lazy="joined")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Thumbnail(db.Model):
    __tablename__ = 'thumbnail'

    thumbnail_id = db.Column(VARCHAR(3), primary_key=True, nullable=False)
    video_id = db.Column(VARCHAR(11), ForeignKey('video.id'), primary_key=True, nullable=False)
    url = db.Column(Text, nullable=True)
    width = db.Column(Integer, nullable=True)
    height = db.Column(Integer, nullable=True)
    resolution = db.Column(VARCHAR(20), nullable=True)
    preference = db.Column(Integer, nullable=True)
    created_at = db.Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    last_updated = db.Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False
    )

    video = relationship('Video', back_populates='thumbnails', lazy="joined")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class VideoFormat(db.Model):
    __tablename__ = 'video_format'

    video_id = db.Column(VARCHAR(11), ForeignKey('video.id'), primary_key=True, nullable=False)
    format = db.Column(VARCHAR(50), ForeignKey('format.format'), primary_key=True, nullable=False)
    quality = db.Column(Integer, nullable=True)
    source_preperence = db.Column(Integer, nullable=True)
    language_preference = db.Column(Integer, nullable=True)
    created_at = db.Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    last_updated = db.Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=True
    )

    video = relationship('Video', back_populates='video_formats', lazy="joined")
    format_rel = relationship('Format', back_populates='video_formats', lazy="joined")

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if self.format_rel:
            data['format_details'] = self.format_rel.as_dict()

        return data

