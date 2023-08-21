from pydantic import BaseModel, EmailStr
 
 
class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
    reset_token: str
 
    class Config:
        orm_mode = True
