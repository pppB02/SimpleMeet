from flask_mail import Message
from app import mail


def sendEmail(subject, recipients, html):
    msg = Message(subject=subject, sender="noreply@simplemeet.com", recipients=[recipients])
    msg.html = html

    mail.send(msg)
    print("Email sent")