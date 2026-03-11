import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
FROM_EMAIL = 'admin@placement_portal.com'

def send_html_email(to_email,subject,html_content):
    msg=MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_mail(to_email,subject,body):
    msg=MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=FROM_EMAIL
    msg["To"]= to_email

    try:
        with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failes to send email : {e}")

def send_file_mail(to_email,subject,body,attachment=None):
    msg = MIMEMultipart()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body))

    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=attachment)

        part['Content-Disposition'] = f'attachment; filename="{attachment}"'
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Failes to send email : {e}")
