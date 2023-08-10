from sqlalchemy import Column,String,Integer,Boolean,Enum, Float
from schema import Roles
from connection import  Base
 
class UserModel(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,unique=True,index=True)
    username=Column(String,unique=True,index=True)
    password=Column(String,unique=False,index=True)
    is_active=Column(Boolean,default=False)
    role=Column(Enum(Roles),default="user")
    
# class ProductModel(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)
#     price = Column(Float)