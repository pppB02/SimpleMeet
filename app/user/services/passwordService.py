import bcrypt


def encrypt(plain_password: str):
    password_hash = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return password_hash.decode("utf-8")


def checkPass(plain_password: str, stored_hash: str) -> bool:
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash)