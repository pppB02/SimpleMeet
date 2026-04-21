from flask import url_for
from ....EmailService import sendEmail
from ....db_models import Business
import os


def MemberAdd(email, name, business_owner_id):
    business = Business.query.filter_by(
            id=business_owner_id).first()

    subject = f"Hi {name}, you've been invited to join {business.name} on SimpleMeet"

    file_path = f"{os.getcwd()}\MailTemplates\invite\index.html"
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    html = file_content.format(business_name=business.name,link=url_for("index.home"))
    
    sendEmail(subject,email,html)