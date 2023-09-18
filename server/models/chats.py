from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
import datetime


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat = Column(String(1000))
    sent_from = Column(String(50), ForeignKey('users.email'))
    sent_to = Column(String(50), ForeignKey('users.email'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_sent_from = relationship('User', back_populates='chats_sent', foreign_keys=[sent_from])
    user_sent_to = relationship('User', back_populates='chats_received', foreign_keys=[sent_to])

    def __init__(self, chat, sent_from, sent_to):
        self.chat = chat
        self.sent_from = sent_from
        self.sent_to = sent_to