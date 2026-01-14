from passlib.context import CryptContext  

# This tells paslin which hashing algorithms we allow
# bcrypt is the one we want

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Takes a plain-text password like "abc123" and returns a bcrypt hash string.
    The returned string includes the salt + algorithm parameters.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Checks whether a plain-text password matches a stored bcrypt hash.
    Returns True if it matches, otherwise False.
    """
    return pwd_context.verify(password, hashed_password)
