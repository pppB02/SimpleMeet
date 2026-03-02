from flask import redirect, flash
from ...db_models import UserAccount

def main(db):
    def encryptPassword(password):
        pass

    def searcInDB(name,email,password):
        newUser = UserAccount(name=name, email=email, password=encryptPassword(password))
        try:
            db.session.add(newUser)
            db.session.commit()
            return redirect("/")
        except:
            return flash("Invalid credentials", "warning")