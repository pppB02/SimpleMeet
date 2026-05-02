from flask import url_for
from ....db_models import Business, Staff, UserAccount
from app import db, serializer
import os


def MemberAdd(email, name, business_owner_id):
    business = Business.query.filter_by(
            admin_user_id=business_owner_id).first()
    
    print(business)
    print(business.id)
    
    token = serializer.dumps({"email":email,"business_id":business.id}, salt="confirmInvite")

    subject = f"Hi {name}, you've been invited to join {business.name} on SimpleMeet"

    file_path = f"{os.getcwd()}\MailTemplates\invite\index.html"
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    #html = file_content.format(business_name=business.name,link=f"http://localhost/confirm-invite/{token}")
    print(f"http://localhost:5000/business/confirm-invite/{token}")
    #sendEmail(subject,email,html)


def confirmInvite(email,datas):
    user = UserAccount.query.filter_by(email=email).first()
    if user.email != datas["email"]:
        print(user.email)
        print(datas["email"])
        raise Exception("The email addresses provided do not match!")
    
    newStaff = Staff(user_id=int(user.id), business_id=int(datas["business_id"]),services={"HELLO":"szia"})
    print(user.id, datas["business_id"])
    try:
        db.session.add(newStaff)
        db.session.commit()
        print("Staff added and saved!")
        return None
    except Exception as e:
        #db.session.rollback()
        print(e)

def verify_token(token):
    return serializer.loads(token, salt="confirmInvite", max_age=3600) #1 óra
    