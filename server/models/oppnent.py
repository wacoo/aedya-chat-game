from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base, engine
from models.users import User

class Opponent(Base):
    ''' opponent class '''
    __tablename__ = 'opponent'
    player_email = Column(String(50), ForeignKey(User.email), primary_key=True)
    opponent_email = Column(String(50), ForeignKey(User.email), primary_key=True)

Base.metadata.create_all(bind=engine)