from flask import redirect
from ....db_models import UserAccount
from ..passwordService import encrypt

def signUpSrv(db, username, email, password):
    if not UserAccount.query.filter_by(email=email).first():
            password_hash, salt = encrypt(password.encode("utf-8"))
            newUser = UserAccount(username=username, email=email, password_hash=password_hash, salt=salt,role="customer")
            try:
                db.session.add(newUser)
                db.session.commit()
                return redirect("/")
            except Exception as e:
                return f"There was an error: {e}"
    else:
        return "That email is already registered"
        
        