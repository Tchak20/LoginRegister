from app.models.database import *
import smtplib
from email.message import EmailMessage
#from twilio.rest import Client

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
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
    
  def resetverify(token, xender):
        email_address = "tchakourabastou@gmail.com" # type Email
        email_password = "wwmbyezukejmaoyd" # If you do not have a gmail apps password, create a new app with using generate password. Check your apps and passwords https://myaccount.google.com/apppasswords

        # create email
        msg = EmailMessage()
        msg['Subject'] = "Email subject"
        msg['From'] = email_address
        msg['To'] = xender # type Email
        msg.set_content(
            f"""\
        Reset password        
        http://127.0.0.1:8000/reset-password/{token}
        """,
                
        )
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)


#Vos identifiants Twilio

    # account_sid = 'AC0fbe1ad0c3374cf8c385ca67ee66e7a8'
    # auth_token = 'f2d4f77097c850d3582c13f2e9e1f091'

    # # Créez un client Twilio
    # client = Client(account_sid, auth_token)

    # # Paramètres pour envoyer un SMS
    # from_number = '+13137697940'
    # to_number = '+22952371203'
    # message =  'http://127.0.0.1:8000/reset-password/{token}'

    # # Envoi du SMS
    # message = client.messages.create(
    #     body=message,
    #     from_=from_number,
    #     to=to_number
    # )

    # print(f"Message sent with SID: {message.sid}")