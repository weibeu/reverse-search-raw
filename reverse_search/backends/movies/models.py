from sqlalchemy import Column, String

from ... import BaseModel


class TitleAKA(BaseModel):

    title_id = Column(String, primary_key=True)

