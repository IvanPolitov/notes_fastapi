from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.database import get_db

from auth_app import schemas
from auth_app import models
from auth_app.utils.auth import create_access_token

auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)
oauth_schema = OAuth2PasswordBearer(tokenUrl='/login')


@auth_router.post('/login', response_model=schemas.Token)
def login(db: Session = Depends(get_db), credentials: schemas.UserLogin = Depends(OAuth2PasswordRequestForm)):
    user = db.query(models.User).filter(
        models.User.username == credentials.username).first()
    user = user
    if user and user.password == credentials.password:
        access_token = create_access_token(
            {'sub': user.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(401, detail='Incorrect username or password')


@auth_router.post('/register', response_model=schemas.UserResponse)
def register(credentials: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        (models.User.username == credentials.username) |
        (models.User.email == credentials.email)
    ).first()

    if user:
        raise HTTPException(
            status_code=400, detail="Email or username already registered")

    new_user = models.User(
        email=credentials.email,
        username=credentials.username,
        password=credentials.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
