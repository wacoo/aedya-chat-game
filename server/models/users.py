from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime

class User(Base):
    __tablename__ = 'users'

    email = Column(String(50), primary_key=True)
    fname = Column(String(50))
    lname = Column(String(50))
    country = Column(String(50))
    score = Column(Integer)
    password = Column(String(200))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    chat = relationship('Chat', back_populates='user')

    def __init__(self, fname, lname, country, score, email, password):
        self.fname = fname
        self.lname = lname
        self.country = country
        self.score = score
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
Base.metadata.create_all(engine)