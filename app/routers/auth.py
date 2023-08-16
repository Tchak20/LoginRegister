from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.emailService import SendEmailVerify
from app.services.userService import  UserRepository
from app.services.scurity import COOKIE_NAME, create_access_token, decode_reset_token, generate_reset_token, get_password_hash, verify_password, verify_token
from sqlalchemy.orm import Session
from DB.connection import  sess_db
from app.models.database import UserModel

AUTH = APIRouter()
templates = Jinja2Templates(directory="templates")

@AUTH.get("/about")
def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
 
@AUTH.get("/email")
def home(request: Request):
    return templates.TemplateResponse("email.html", {"request": request})
 
 
@AUTH.get("/user/signup")
def signup(req: Request):
    return templates.TemplateResponse("signup.html", {"request": req})
 
@AUTH.post("/signupuser")
def signup_user(db:Session=Depends(sess_db),username : str = Form(),email:str=Form(),password:str=Form()):
    userRepository=UserRepository(db)
    db_user= userRepository.get_user_by_username(username)
    if db_user:
        return "username is not valid"
 
    signup=UserModel(email=email,username=username,password=get_password_hash(password))
    success=userRepository.create_user(signup)
    create_access_token(signup)
    token=create_access_token(signup)
    SendEmailVerify.sendVerify(token,email)
    if success:
        return "create  user successfully"
    else:
        raise HTTPException(
            status_code=401, detail="Credentials not correct"
        )
 
@AUTH.get("/user/signin")
def login(req: Request):
    return templates.TemplateResponse("/signin.html", {"request": req})
 
@AUTH.post("/signinuser")
def signin_user(response:Response,db:Session=Depends(sess_db),username : str = Form(),password:str=Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "username or password is not valid"
 
    if verify_password(password,db_user.password):
        token=create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return {COOKIE_NAME:token,"token_type":"bastoucoders"}
 
@AUTH.get('/user/verify/{token}')
def verify_user(token,db:Session=Depends(sess_db)):
    userRepository=UserRepository(db)
    payload=verify_token(token)
    username=payload.get("username")
    db_user=userRepository.get_user_by_username(username)
 
    if not username:
        raise  HTTPException(
            status_code=401, detail="Credentials not correct"
        )
    if db_user.is_active==True:
        return "your account  has been allreay activeed"
 
    db_user.is_active=True
    db.commit()
    response=RedirectResponse(url="/user/signin")
    return response
    #http://127.0.0.1:8000/user/verify/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNseWRleTAxMzEiLCJlbWFpbCI6ImNseWRleUBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImFjdGl2ZSI6ZmFsc2V9.BKektCLzr47qn-fRtnGVulSdYlcMdemJQO_p32jWDk0

@AUTH.post("/reset")
def verify_mail(db:Session=Depends(sess_db),email:str=Form()):
    userRepository = UserRepository(db)
    user = userRepository.get_user_by_email(email) 
    if user:
        token = generate_reset_token(email)
        user.reset_token = token
        db.commit()
        SendEmailVerify.resetverify(token,email)
        return {"message": "Password reset email sent"}
    return {"message": "User not found"}

@AUTH.get('/reset-password/{token}')
def reset_password(request: Request,token,db:Session=Depends(sess_db)):
    userRepository=UserRepository(db)
    payload=token
    reset_token = userRepository.get_user_by_reset_token(payload)
    reset_password = {
        "reset": reset_token.username
    }
    if not reset_token:
        raise  HTTPException(
            status_code=401, detail="Credentials not correct"
        )
    else:
        return templates.TemplateResponse("reset.html", {"request": request, **reset_password})
    
@AUTH.post('/new-password/{reset_token}')
def new_password(reset_token,request: Request,newpassword : str = Form(),confirmpassword:str=Form(),db:Session=Depends(sess_db)):
    userRepository=UserRepository(db)
    reset_tokenf = userRepository.get_user_by_username(reset_token)
    if newpassword == confirmpassword:
        reset_tokenf.password = get_password_hash(newpassword)
        db.commit()
        return  templates.TemplateResponse("signin.html", {"request": request})
    else:   
        return {"message": "Les mots de passe incorrect"}
    