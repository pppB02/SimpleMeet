import bcrypt

def encrypt(password:str):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt)
    return password_hash, salt

def checkPass(plain_password,salt,bd_password)->bool:
    password_hash = bcrypt.hashpw(plain_password, salt)
    return True if bd_password==password_hash else False