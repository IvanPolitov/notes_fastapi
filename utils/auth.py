from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.database import get_db

from models import User
from schemas import TokenData


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = "mysecretkey"


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')
security = HTTPBearer()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={'WWW-Authenticate': 'Bearer'}
    )
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    try:
        token = token.replace("Bearer ", '')
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
    user = db.query(User).filter(
        token_data.username == User.username).first()
    if user:
        return user
    raise credentials_exception
