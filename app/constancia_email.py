import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def constancia_email(pdf, email):
    fromaddr = "braavosi@outlook.es"
    toaddr = email

    # MIMEMultipart 
    msg = MIMEMultipart() 
  
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = "Constancia Monotributo"
    body = "Constancia Monotributo Descargada"
      