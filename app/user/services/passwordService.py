import bcrypt

def encrypt(password:str):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password, salt).decode("utf-8")
    return password_hash, salt

def checkPass(plain_password,salt,db_password)->bool:
    password_hash = bcrypt.hashpw(plain_password, salt)
    print("plain_password",plain_password)
    print("password_hash",password_hash)
    print("PassService:")
    print(True if db_password==password_hash else False)
    print("--------------")
    return True if db_password==password_hash else False