from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Constants
SECRET_KEY = os.getenv("ENCRYPTION_KEY")  # Load the secret key from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create a token
def create_access_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decode and validate the token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
