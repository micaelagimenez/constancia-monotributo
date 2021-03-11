from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import boto

def constancia_email(email):

        msg = MIMEMultipart()
        msg['Subject'] = 'Constancia Monotributo'
        msg['From'] = ''
        msg['To'] = email

        msg.preamble = 'Multipart message.\n'

        # msg body
        part = MIMEText('')
        msg.attach(part)

        # pdf
        part = MIMEApplication(open('constancia.pdf','rb').read())
        part.add_header('Content-Disposition', 'attachment', filename='constancia.pdf')
        msg.attach(part)

        #  SES
        connection = boto.connect_ses(aws_access_key_id=''
            , aws_secret_access_key='')

        # send
        result = connection.send_raw_email(msg.as_string()
            , source=msg['From']
            , destinations=[msg['To']])
        
        print(result)

