from sqlalchemy.orm import Session
from app.models.database import  UserModel
from app.models.database import *
from typing import  Dict,Any
import smtplib
from email.message import EmailMessage
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


 
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
    
    def get_user_by_email(self,email: str):
        return self.sess.query(UserModel).filter(UserModel.email==email).first()
    def get_user_by_reset_token(self,reset_token: str):
        return self.sess.query(UserModel).filter(UserModel.reset_token==reset_token).first()
    def get_user_by_password(self,password: str):
        return self.sess.query(UserModel).filter(UserModel.password==password).first()
 
    def update_user(self, email: str, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(UserModel).filter(UserModel.email == email).update(details, synchronize_session=False)
            self.sess.commit()
        except SQLAlchemyError as e:
            print("Erreur SQLAlchemy:", str(e))
            self.sess.rollback()  # Annule les modifications en cas d'erreur
            return False
        return True
    def delete_user(self,id:int)-> bool:
        try:
            self.sess.query(UserModel).filter(UserModel.id==id).delete()
            self.sess.commit()
        except:
            return  False
        return  True