from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime
from models.chats import Chats

class User(Base):
    __tablename__ = 'users'
    email = Column(String(50), primary_key=True)
    fname = Column(String(50))
    lname = Column(String(50))
    country = Column(String(50))
    score = Column(Integer)
    password = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    chats_sent = relationship('Chats', back_populates='user_sent_from', foreign_keys='Chats.sent_from')
    chats_received = relationship('Chats', back_populates='user_sent_to', foreign_keys='Chats.sent_to')

    def __init__(self, fname, lname, country, score, email, password):
        self.fname = fname
        self.lname = lname
        self.country = country
        self.score = score
        self.email = email
        self.password = password

#Base.metadata.create_all(engine)