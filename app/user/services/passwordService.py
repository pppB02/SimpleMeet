import bcrypt

def encrypt(password:str):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

def checkPass(password):
    return bcrypt.checkpw(password,encrypt(password))