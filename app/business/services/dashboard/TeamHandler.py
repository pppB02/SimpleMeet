from ....db_models import Business, Staff, UserAccount, StaffIviteLinks
from app import db, serializer
import os


def MemberAdd(email, name, business_owner_id, pfp):
    business = Business.query.filter_by(admin_user_id=business_owner_id).first()

    if not business:
        raise ValueError("Business not found")

    if StaffIviteLinks.query.filter_by(email=email).first():
        print("An invite already sent to this email")
        return None

    token = serializer.dumps(
        {"email": email, "business_id": business.id, "pfp_name": pfp},
        salt="confirmInvite"
    )

    newLink = StaffIviteLinks(email=email, token=token)

    try:
        db.session.add(newLink)
        db.session.commit()
        print("Invite link saved!")
    except Exception as e:
        db.session.rollback()
        print(e)
        raise

    subject = f"Hi {name}, you've been invited to join {business.name} on SimpleMeet"
    file_path = os.path.join(os.getcwd(), "MailTemplates", "invite", "index.html")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    else:
        file_content = "<p>You are invited.</p><a href='{{invite_link}}'>Join</a>"

    invite_link = f"http://localhost:5000/business/confirm-invite/{token}"
    print(invite_link)

    # ha van EmailService, akkor itt lehetne elküldeni
    # sendEmail(subject, email, html)

    return token


def confirmInvite(email, datas):
    user = UserAccount.query.filter_by(email=email).first()

    if not user:
        raise ValueError("User not found")

    if user.email != datas["email"]:
        raise ValueError("The email addresses provided do not match!")

    inviteLink = StaffIviteLinks.query.filter_by(email=email).first()
    if not inviteLink:
        raise ValueError("The invite used or expired!")

    newStaff = Staff(
        user_id=int(user.id),
        business_id=int(datas["business_id"]),
        pfp_name=datas["pfp_name"]
    )

    try:
        db.session.add(newStaff)
        db.session.delete(inviteLink)
        db.session.commit()
        print("Staff added and saved!")
        return None
    except Exception as e:
        db.session.rollback()
        print(e)
        raise


def verify_token(token):
    return serializer.loads(token, salt="confirmInvite", max_age=3600)