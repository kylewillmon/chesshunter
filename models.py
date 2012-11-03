#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    white = Column(String)
    black = Column(String)

class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True)
    move_num = Column(Integer)
    game_id = Column(Integer, ForeignKey("games.id"))
    game = relationship('Game', backref=backref('moves',
                           order_by=move_num))
    src = Column(String)
    dst = Column(String)

    __table_args__ = ( UniqueConstraint('game_id', 'move_num'), )

def initialize_sql(engine):
    Base.metadata.create_all(engine)
