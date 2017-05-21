# -*- coding: utf-8 -*-
import os

from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import validates


import getpass
username = getpass.getuser()
engine = create_engine("postgresql:///%s"%username)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean, default=False)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    text = Column(String)


Base.metadata.create_all(engine)
