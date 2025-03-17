from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.database import get_db

from schemas import UserCreate, UserResponse
from models import User
from utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)


@auth_router.post('/login')
def login(response: Response,
          db: Session = Depends(get_db),
          credentials: OAuth2PasswordRequestForm = Depends()
          ):

    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not user.password == credentials.password:
        raise HTTPException(401, detail='Incorrect username or password')

    access_token = create_access_token({'sub': user.username})
    response.set_cookie(
        key="access_token",
        value=f'Bearer {access_token}',
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite='lax',
        secure=True
    )
    return {"message": "Welcome, cookies set"}


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


@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}
