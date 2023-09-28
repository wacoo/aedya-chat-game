from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, engine
import datetime

class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(1000))
    player1 = Column(String(50), ForeignKey('users.email'))
    player2 = Column(String(50), ForeignKey('users.email'))
    winner = Column(String(50))
    done = Column(Boolean)
    chat_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, name, description, player1, player2, winner='', done=False):
        self.name = name
        self.description = description
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.done = done
        self.chat_count = 0
Base.metadata.create_all(bind=engine)