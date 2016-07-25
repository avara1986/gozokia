import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

from gozokia.conf import settings
from gozokia.db.base import ModelBase


class Chat(Base):
    __tablename__ = 'gozokia_chat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, nullable=True)
    session = Column(String(250), nullable=False)
    text = Column(String(250), nullable=False)
    type_rule = Column(String(1), nullable=False)
    rule = Column(String(250), nullable=True)
    status = Column(String(250), nullable=True)


class Database(ModelBase):

    def __init__(self):
        self.engine = create_engine('sqlite:///db.sqlite3')
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

        DBSession = sessionmaker(bind=self.engine)
        self.db = DBSession()

    def get(self, key=None, search=None):
        pass

    def set(self, *args, **kwargs):
        pass

    def set_chat(self, *args, **kwargs):
        """
        {'user': self.user_id, 'session': self.session_id,
                                    'text': self.sentence, 'type_rule': 'I',
                                    'rule': None, 'status': None}

        """
        kwargs['session'] = str(kwargs['session'])
        new_chat = Chat(**kwargs)
        self.db.add(new_chat)
        self.db.commit()

    def get_chat(self, session, user=None):
        return self.db.query(Chat).all()
