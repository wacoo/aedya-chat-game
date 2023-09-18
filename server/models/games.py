from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, engine
import datetime

class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    description = Column(String(1000))
    user_email = Column(String(50), ForeignKey('users.email'))
    # user = relationship('User', back_populates='notes')

    def __init__(self, title, content, user_email):
        self.title = title
        self.content = content
        self.user_email = user_email
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
Base.metadata.create_all(engine)