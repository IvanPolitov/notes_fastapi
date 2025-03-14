from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.database import get_db

from schemas import UserCreate, Token, UserResponse
from models import User
from utils.auth import create_access_token

auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@auth_router.post('/login', response_model=Token)
def login(db: Session = Depends(get_db), credentials: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(
        User.username == credentials.username).first()
    if user and user.password == credentials.password:
        access_token = create_access_token(
            {'sub': user.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(401, detail='Incorrect username or password')


@auth_router.post('/register', response_model=UserResponse)
def register(credentials: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == credentials.username) |
        (User.email == credentials.email)
    ).first()

    if user:
        raise HTTPException(
            status_code=400, detail="Email or username already registered")

    new_user = User(
        email=credentials.email,
        username=credentials.username,
        password=credentials.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
