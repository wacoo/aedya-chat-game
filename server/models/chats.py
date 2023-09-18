from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime

class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat = Column(String(1000))
    sent_to = Column(String(50), ForeignKey('users.email'))
    user = relationship('User', back_populates='chats')

    def __init__(self, chat, user_email):
        self.chat = chat
        self.user_email = user_email
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
Base.metadata.create_all(engine)