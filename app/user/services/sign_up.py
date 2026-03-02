from flask import redirect, flash
from ...db_models import UserAccount
from .passwordService import encrypt, checkPass

def service(db, name, email, password):
    print(UserAccount.query.filter_by(email=email).first())
    newUser = UserAccount(name=name, email=email, password_hash=encrypt(password.encode("utf-8")),role="customer")
    try:
        db.session.add(newUser)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was an error: {e}"