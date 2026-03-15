from flask import redirect, render_template
from flask_login import login_user, current_user
from ....db_models import UserAccount
from ..passwordService import checkPass

def loginSrv(email, password, remember):
    user = UserAccount.query.filter_by(email=email).first()
    if user and checkPass(password,user.salt,user.password_hash):
            login_user(user, remember=remember)
            print("login was succesfull")
            return None
    else:
        raise Exception("bad password or email")