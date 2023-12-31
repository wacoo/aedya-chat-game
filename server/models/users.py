from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime

class User(Base):
    ''' user class '''
    __tablename__ = 'users'
    email = Column(String(50), primary_key=True)
    fname = Column(String(50))
    lname = Column(String(50))
    country = Column(String(50))
    total_score = Column(Integer)
    password = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    games_as_player1 = relationship('Games', backref='player1_user', foreign_keys='Games.player1')
    games_as_player2 = relationship('Games', backref='player2_user', foreign_keys='Games.player2')

    chats_sent = relationship('Chats', back_populates='user_sent_from', foreign_keys='Chats.sent_from')
    chats_received = relationship('Chats', back_populates='user_sent_to', foreign_keys='Chats.sent_to')

    def __init__(self, fname, lname, email, password, country='', total_score=0):
        self.fname = fname
        self.lname = lname
        self.country = country
        self.total_score = total_score
        self.email = email
        self.password = password

# Create the table in the database
Base.metadata.create_all(bind=engine)