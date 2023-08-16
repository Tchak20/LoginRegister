from sqlalchemy import Column,String,Integer,Boolean,Enum, Float
from DB.connection import  Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    #role = Column(Enum('user', 'admin'), default='user')
    reset_token = Column(String(400), default='NULL')