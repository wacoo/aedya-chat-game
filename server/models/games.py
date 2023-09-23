from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime

class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    description = Column(String(1000))
    player1 = Column(String(50), ForeignKey('users.email'))
    player2 = Column(String(50), ForeignKey('users.email'))
    winner = Column(String(50))
    done = Column(Boolean)
    #user_email = Column(String(50), ForeignKey('users.email'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    # user = relationship('User', back_populates='notes')
    user_player1 = relationship('User', back_populates='games_as_player1', foreign_keys=[player1])
    user_player2 = relationship('User', back_populates='games_as_player2', foreign_keys=[player2])
    def __init__(self, name, description, player1, player2, winner='', done=False):
        self.name = name
        self.description = description
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.done = done

Base.metadata.create_all(engine)