from pydantic import BaseModel, EmailStr #pip install pydantic[email]
from enum import Enum
 
 
class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    reset_token: str
 
    class Config:
        orm_mode = True
 
# class Roles(Enum):
#     user = "user"
#     admin = "admin"
    