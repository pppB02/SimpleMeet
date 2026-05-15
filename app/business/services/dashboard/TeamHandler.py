from ....db_models import Business, Staff, UserAccount, StaffIviteLinks
from app import db, serializer
import os


def MemberAdd(email, name, business_owner_id, pfp):
    business = Business.query.filter_by(
            admin_user_id=business_owner_id).first()
    
    print(business)
    print(business.id)

    if StaffIviteLinks.query.filter_by(email=email).first():
        print("An invite already sent to this email")
        return None

    token = serializer.dumps({"email":email,"business_id":business.id,"pfp_name":pfp}, salt="confirmInvite")
    newLink = StaffIviteLinks(email=email, token=token)
    try:
        db.session.add(newLink)
        db.session.commit()
        print("Invite link saved!")
    except Exception as e:
        #db.session.rollback()
        print(e)
    
    
    
    
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
    
    inviteLink = StaffIviteLinks.query.filter_by(email=email).first()
    if not inviteLink:
        print("The invite used or expired!")
    
    newStaff = Staff(user_id=int(user.id), business_id=int(datas["business_id"]),services={"HELLO":"szia"},pfp_name=datas["pfp_name"])
    print(user.id, datas["business_id"])
    try:
        db.session.add(newStaff)
        db.session.delete(inviteLink)
        db.session.commit()
        print("Staff added and saved!")
        return None
    except Exception as e:
        #db.session.rollback()
        print(e)

def verify_token(token):
    return serializer.loads(token, salt="confirmInvite", max_age=3600) #1 óra
    