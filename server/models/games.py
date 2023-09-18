from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime

class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    description = Column(String(1000))
    #user_email = Column(String(50), ForeignKey('users.email'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    # user = relationship('User', back_populates='notes')

    def __init__(self, name, description):
        self.name = name
        self.description = description
        #self.user_email = user_email

Base.metadata.create_all(engine)