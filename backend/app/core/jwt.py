from datetime import datetime, timedelta, timezone 
from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(subject: str) -> str: 
    """
    subject: usually the user_id (as a string)
    returns: JWT string
    """  
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict: 
    """
    returns the decoded payload if valid, otherwise raises JWTError
    """
    return jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
