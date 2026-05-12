import hashlib
import hmac


# NOTE: Replace with a strong password hasher (e.g., passlib) before production.
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)
