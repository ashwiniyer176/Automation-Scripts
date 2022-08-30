"""
A Python script to automate the process of sending my downloaded .mobi files to my Kindle device
"""


import os
import math
import smtplib
import random
from dotenv import load_dotenv, find_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders

load_dotenv(find_dotenv())


def setup_message(sender, receiver, attachment):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = ""

    attach_file = open(attachment, "rb")
    payload = MIMEApplication(attach_file.read(), Name=attachment.split("/")[-1])
    payload["Content-Disposition"] = (
        'attachment; filename="%s"' % attachment.split("/")[-1]
    )
    message.attach(payload)
    return message


if __name__ == "__main__":
    SENDER = os.environ["GMAIL_ID"]
    SENDER_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
    RECEIVER = os.environ["KINDLE_EMAIL_ID"]
    ATTACHMENT = "books\The Checklist Manifesto How to Get Things Right by Gawande Atul (z-lib.org).mobi"
    session = smtplib.SMTP("smtp.gmail.com", 587)
    message = setup_message(SENDER, RECEIVER, ATTACHMENT)
    text = message.as_string()
    session.starttls()
    session.login(SENDER, SENDER_PASSWORD)
    session.sendmail(SENDER, [RECEIVER, SENDER], text)
    print("Message sent")
    session.quit()
