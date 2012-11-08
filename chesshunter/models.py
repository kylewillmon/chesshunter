#!/usr/bin/env python

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()
DBSession = sessionmaker()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    __table_args__ = ( UniqueConstraint('username'), )

    @staticmethod
    def new(username, password):
        return User(username=username,
                password=bcrypt.hashpw(password, bcrypt.gensalt()))

    def __json__(self):
        return {'id': self.id,
                'username': self.username}

    def check_password(self, password):
        hashed = bcrypt.hashpw(password, self.password)
        return (hashed == self.password)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    board = Column(String)
    white_id = Column(Integer, ForeignKey("users.id"))
    white = relationship("User", primaryjoin='Game.white_id==User.id')
    black_id = Column(Integer, ForeignKey("users.id"))
    black = relationship("User", primaryjoin='Game.black_id==User.id')

    def __json__(self):
        return {'id': self.id,
                'white': self.white.__json__(),
                'black': self.black.__json__(),
                'board': self.board,
                'moves': [x.__json__() for x in self.moves]}

class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True)
    move_num = Column(Integer)
    game_id = Column(Integer, ForeignKey("games.id"))
    game = relationship('Game', backref=backref('moves',
                           order_by=move_num))
    src = Column(String)
    dst = Column(String)

    def __json__(self):
        return [self.src, self.dst]

    __table_args__ = ( UniqueConstraint('game_id', 'move_num'), )

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
