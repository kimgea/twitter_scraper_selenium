'''
Created on 25. nov. 2015

@author: kga

Create database ovject by inspecting existing databse tables

'''

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sbot.twitter.scraper.config as config
 
engine = create_engine(config.get_database_string())
Base = declarative_base(engine)

class User(Base):
    __tablename__ = 't_user'
    __table_args__ = {'autoload':True}

class Friendship(Base):
    __tablename__ = 't_friendship'
    __table_args__ = {'autoload':True}
    
class Tweets(Base):
    __tablename__ = 't_tweet'
    __table_args__ = {'autoload':True}

 
#----------------------------------------------------------------------
def load_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
