from flask import redirect, render_template
from ...db_models import UserAccount
from .passwordService import checkPass

def loginSrv(db, name, email, password):
    user = UserAccount.query.filter_by(email=email).first()
    print(user)
    if user != None:
        if checkPass(password,user.salt,user.password_hash):
            print("login was succesfull")
            return redirect("admin/")
        else:
            return render_template("login/login.html",error="wrong password")
    else:
        return "<p>This email address has not been registered yet. <a href='sign-up'>Sing up</a></p>"