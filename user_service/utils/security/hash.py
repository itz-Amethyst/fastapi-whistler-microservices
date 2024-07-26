import base64
import hashlib
import secrets
from user_service.config import settings

def hash_password(password, salt=None, iterations=600000):
        if salt is None:
            salt = secrets.token_hax(16)
        assert salt and isinstance(salt, str) and "$" not in salt
        assert isinstance(password, str)
        pw_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
        )
        b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
        return "{}${}${}${}".format(settings.PASSWORD_HASH_ALGORITHM , iterations, salt, b64_hash)

def verify_password(password, password_hash) -> bool:
    if (password_hash or "").count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = password_hash.split("$", 3)
    iterations = int(iterations)
    assert algorithm == settings.PASSWORD_HASH_ALGORITHM
    compare_hash = hash_password(password, salt, iterations)
    return secrets.compare_digest(password_hash, compare_hash)