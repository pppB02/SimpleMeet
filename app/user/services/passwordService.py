import bcrypt

def encrypt(plain_password:str):
    password_hash = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
    return password_hash

def checkPass(plain_password:str,stored_hash:str)->bool:
    return bcrypt.checkpw(plain_password.encode(),stored_hash) 