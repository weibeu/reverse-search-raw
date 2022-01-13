from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from . import config

from datetime import datetime
from abc import abstractmethod


def __get_connection_string():
    config_ = config.POSTGRESQL
    prefix = "{db_url}://{user}".format(db_url=config_["url"], user=config_["username"])
    suffix = "{host}:{port}/{db}".format(host=config_["host"], port=config_["port"], db=config_["db"])
    prefix += ":{0}".format(config_["password"]) if config_["password"] else str()

    return "{0}@{1}".format(prefix, suffix)


def get_database_engine():
    connection_string = __get_connection_string()
    return create_async_engine(connection_string, **config.POSTGRESQL["pool"])


Session = sessionmaker(bind=get_database_engine(), class_=AsyncSession)


class SessionContext(object):

    def __init__(self):
        self._session_factory = async_scoped_session(Session)
        self.session = self._session_factory()

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.commit()
        await self.session.close()
        await self._session_factory.remove()


class __ModelMeta(DeclarativeMeta):

    ELASTICSEARCH_INDEX = None

    def __init__(cls, *args, **kwargs):
        if cls.ELASTICSEARCH_INDEX:
            cls.insertion_time = Column(DateTime, default=datetime.utcnow, nullable=False)
            cls.modification_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
        super().__init__(*args, **kwargs)


class __BaseModel(object):

    @property
    @abstractmethod
    def elasticsearch_document(self):
        if not self.ELASTICSEARCH_INDEX:
            raise AttributeError
        raise NotImplementedError


BaseModel = declarative_base(cls=__BaseModel, metaclass=__ModelMeta)
