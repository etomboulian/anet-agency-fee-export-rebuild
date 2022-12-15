import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

# SMTP configuration
class SMTPSettings(Enum):
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = os.environ.get('SMTP_PORT')
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    target_email = os.environ.get('TARGET_EMAIL')

def email_results(file_name):
    # Create the message
    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = SMTPSettings.sender_email.value
    msg['To'] = SMTPSettings.target_email.value
    msg.attach(MIMEText(open(os.path.join(os.getcwd(), os.environ.get('OUTPUT_PATH'), file_name)).read()))

    # send the message
    with smtplib.SMTP(SMTPSettings.smtp_server.value, SMTPSettings.smtp_port.value) as server:
        server.ehlo()
        server.login(
            login=SMTPSettings.sender_email.value, 
            password=SMTPSettings.sender_password.value)
        server.sendmail(
            from_addr=SMTPSettings.sender_email.value, 
            to_addrs=SMTPSettings.target_email.value, 
            msg=msg.as_string()
            )