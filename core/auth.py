import hashlib, hmac, os


def hash_password(password, salt=None):
    salt = salt or os.urandom(16).hex()
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()
    return h, salt


def verify_password(password, pw_hash, salt):
    h, _ = hash_password(password, salt)
    return hmac.compare_digest(h, pw_hash)