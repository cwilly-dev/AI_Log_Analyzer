from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)

ALGORITHM = settings.ALGORITHM

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_minutes: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)