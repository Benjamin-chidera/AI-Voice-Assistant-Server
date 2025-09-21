from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def create_access_token(fullname: str, user_id: int):
    payload = {
        "sub": fullname,
        "id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # ✅ keyword
    return token
