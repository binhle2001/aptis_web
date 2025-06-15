from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Settings from .env
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY must be set in the environment variables.")

class TokenData(BaseModel):
    sub: Optional[str] = None # username
    user_id: Optional[int] = None
    role: Optional[str] = None
    fullname: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenData : # Trả về TokenData thay vì TokenDataSchema
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Tạo instance TokenData từ payload
        # Các trường không có trong payload sẽ là None do Optional
        token_data = TokenData(**payload)
        if token_data.sub is None: # username (sub) là bắt buộc
            return None
        return token_data
    except JWTError:
        return None

# Placeholder for user data - In a real app, this would come from the database
# DUMMY_USERS_DB = {
#     "admin": {
#         "username": "admin",
#         "fullname": "Admin User",
#         "password_hash": get_password_hash("admin123"), # Store hashed passwords
#         "role": "admin",
#         "is_active": True
#     },
#     "member1": {
#         "username": "member1",
#         "fullname": "Member One",
#         "password_hash": get_password_hash("member123"),
#         "role": "member",
#         "is_active": True
#     }
# }

# def get_user_from_db(username: str):
#     if username in DUMMY_USERS_DB:
#         user_dict = DUMMY_USERS_DB[username]
#         # In a real app, you might map this to a Pydantic model or User object
#         return user_dict
#     return None