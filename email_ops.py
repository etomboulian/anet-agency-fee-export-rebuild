import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# SMTP configuration
smtp_server = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT')
sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')
target_email = os.environ.get('TARGET_EMAIL')

def email_results(file_name):
    # Create the message
    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = sender_email
    msg['To'] = target_email
    msg.attach(MIMEText(open(os.path.join(os.getcwd(), os.environ.get('OUTPUT_PATH'), file_name)).read()))

    # send the message
    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, msg.as_string())