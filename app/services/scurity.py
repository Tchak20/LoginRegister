from passlib.context import  CryptContext 
from fastapi.security import OAuth2PasswordBearer
from jose import jwt 
from fastapi import Depends,Request
import secrets
import base64
 
from app.models.database import UserModel

 
JWT_SECRET="cairocoders$§%§$Ednalan"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=3000
 
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") #pip install bcrypt
# save token to oauth2_scheme
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="user/signin")
COOKIE_NAME="Authorization"
 
# create Token
def create_access_token(user):
    try:
        payload={
            "username":user.username,
            "email":user.email,
            "active":user.is_active,
            "reset_token":user.reset_token
        }
        return  jwt.encode(payload,key=JWT_SECRET,algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex
 
# create verify Token
def verify_token(token):
    try:
        payload=jwt.decode(token,key=JWT_SECRET)
        return payload
    except Exception as ex:
        print(str(ex))
        raise ex
 
# password hash
def  get_password_hash(password):
    return pwd_context.hash(password)
 
# password verify
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
 
def get_current_user_from_token(token:str=Depends(oauth2_scheme)):
    user= verify_token(token)
    return user
 
def get_current_user_from_cookie(request:Request) -> UserModel:
    token=request.cookies.get(COOKIE_NAME)
    if token:
        user = verify_token(token)
        return user
    
#Token reset
def generate_reset_token(email):
    token = secrets.token_urlsafe(32)
    print(email)
    print(token)
    return token

def decode_reset_token(encoded_token):
    try:
        token_bytes = base64.urlsafe_b64decode(encoded_token + '==')
        decoded_token = token_bytes.decode('utf-8')
        return decoded_token
    except Exception as e:
        print("Error decoding token:", e)
        return None
