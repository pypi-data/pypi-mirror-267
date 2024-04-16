from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key to sign the tokens
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "9b73f2a1bdd7ae163444473d29a6885ffa22ab26117068f72a5a56a74d12d1fc")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
# Token expiration time
TOKEN_EXPIRATION = datetime.utcnow() + timedelta(hours=24)

# Function to create JWT tokens
def create_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": TOKEN_EXPIRATION
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# Function to validate JWT tokens
async def check_access_token(credentials: HTTPBasicCredentials = Depends(HTTPBearer())):
    """
        Function that is used to validate the token in the case that it requires it
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if payload is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
    


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
