from sqlalchemy import Column, String, Integer, Boolean, Enum

from ... import BaseModel
from .enums import TitleType


class TitleAKA(BaseModel):

    title_id = Column(String, )
    ordering = Column(Integer, )
    title = Column(String, )
    region = Column(String, )
    language = Column(String, )
    types = Column(Enum(TitleType, ), )
    attributes = Column(String, )
    is_original_title = Column(Boolean, )


class TitleBasics(BaseModel):

    title_id = Column(String, primary_key=True)
    title_type = Column(String, )
    primary_title = Column(String, )
    original_title = Column(String, )
    is_adult = Column(Boolean, )
    start_year = Column(Integer, )
    end_year = Column(Integer, )
    runtime_minutes = Column(Integer, )
    genres = Column(String, )
