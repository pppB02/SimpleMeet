from flask import redirect, render_template
from flask_login import login_user
from ....db_models import UserAccount
from ..passwordService import encrypt

def signUpSrv(db, username, email, password,role):
    newUser = UserAccount(username=username, email=email, password_hash=encrypt(password), role=role)
    try:
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        print("sing up was succesfull")
        return None
    except Exception as e:
        return e
