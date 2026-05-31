from flask_login import login_user
from ....db_models import UserAccount
from ..passwordService import encrypt


def signUpSrv(db, username, email, password, role):
    newUser = UserAccount(
        username=username,
        email=email,
        password_hash=encrypt(password),
        role=role
    )

    try:
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        print("sign up was successfull")
        return None
    except Exception as e:
        db.session.rollback()
        raise e