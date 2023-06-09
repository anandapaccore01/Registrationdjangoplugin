from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import jwt
import random
import string


def sendemail(users):      
    to = users.email
    name = users.username
    
    subject = 'Welcome to Real Returns Project'
    values = '<p>Hello #NAME#,</p><p>Your account has been created.</p><p>Your login credentials :</p><p>Email: #EMAIL#</p><p>Please click the link to verify your email.</p><p>Thank you,</p><p>&nbsp;</p>'
    values = values.replace('#NAME#',name)
    values = values.replace('#EMAIL#',to)
    
    now=datetime.now().timestamp()
   
    duration =timedelta(minutes=1).total_seconds()    
    expiration = now + duration
    payload = {
        'user_id' : users.id,
        'expiry' : expiration,
    }    
    token = jwt.encode(payload, settings.SECRET_KEY,algorithm='HS256')    
    activation_link = f'http://127.0.0.1:8000/emailactivate/{token}'    
    html_content = render_to_string("email_welcome.html", {'content':values, 'content1':activation_link}) 
    email = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [to])
    email.attach_alternative(html_content,'text/html')
    email.send()

def sendchangeemail(email,users):
    to = email    
    name = users.username 
    subject='Account Email Change Request'
    change_email='<p>Hello #NAME#,</p><p>We have email change for your account.</p><p>Your login credentials :</p><p>Your Previous Email: #EMAIL#</p><p>Please click the link to verify new your email.After Successful verification you can use your new email to login</p><p>Thank you,</p><p>Paccore Python Team</p>'
    change_email = change_email.replace('#NAME#',name)
    change_email = change_email.replace('#EMAIL#',users.email)
    now=datetime.now().timestamp()   
    duration =timedelta(minutes=1).total_seconds()    
    expiration = now + duration
    payload = {
        'user_id' : users.id,
        'expiry' : expiration,
    }    
    token = jwt.encode(payload, settings.SECRET_KEY,algorithm='HS256') 
    activation_link = f'http://127.0.0.1:8000/emailactivate/{token}' 
    
    html_content = render_to_string("email_welcome.html", {'content':change_email, 'content1':activation_link}) 

    email = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [to])
    email.attach_alternative(html_content,'text/html')
    email.send()

def  send_resetpasswordemail(users,token):
    to = users.email  
    name = users.username    
    subject = 'Real returns:Reset Your Password'
    values = "<p>Hello #NAME#,</p><p>You've asked us to reset password.</p> <p>Please click on the below button to enter your new password</p><p>&nbsp;</p>"
    values = values.replace('#NAME#',name)
    dt=datetime.now().time()
    timespan=dt.hour*3600+dt.minute*60+dt.second
    verify_string="".join(random.choices(string.ascii_letters+string.digits,k=20))
    

    Resetpassword_link = f'http://127.0.0.1:8000/resetpassword?user_id={users.id}&timespan={timespan}&token={token}'
    html_content = render_to_string("email_password.html", {'content':values, 'content1':Resetpassword_link}) 

    email = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [users.email])
    email.attach_alternative(html_content,'text/html')
    email.send()