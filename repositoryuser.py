from sqlalchemy.orm import Session
from models import  UserModel
from models import *
from typing import  Dict,Any
from sqlalchemy.orm import Session
 
import smtplib
from email.message import EmailMessage

 
class UserRepository:
    def __init__(self,sess:Session):
        self.sess: Session=sess
 
    def create_user(self,signup:UserModel) -> bool:
         try:
             self.sess.add(signup)
             self.sess.commit()
         except:
             return False
         return True
 
    def get_user(self):
        return  self.sess.query(UserModel).all()
 
    def get_user_by_username(self,username:str):
        return self.sess.query(UserModel).filter(UserModel.username==username).first()
 
    def update_user(self,id:int,details:Dict[str,Any]) -> bool:
        try:
            self.sess.query(UserModel).filter(UserModel.id==id).update(details)
            self.sess.commit()
        except:
            return False
        return True
    def delete_user(self,id:int)-> bool:
        try:
            self.sess.query(UserModel).filter(UserModel.id==id).delete()
            self.sess.commit()
        except:
            return  False
        return  True
 
class SendEmailVerify:
 
  def sendVerify(token, xender):
    email_address = "tchakourabastou@gmail.com" # type Email
    email_password = "wwmbyezukejmaoyd" # If you do not have a gmail apps password, create a new app with using generate password. Check your apps and passwords https://myaccount.google.com/apppasswords
 
    # create email
    msg = EmailMessage()
    msg['Subject'] = "Email subject"
    msg['From'] = email_address
    msg['To'] = xender # type Email
    msg.set_content(
       f"""\
    verify account        
    http://127.0.0.1:8000/user/verify/{token}
    """,
         
    )
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)