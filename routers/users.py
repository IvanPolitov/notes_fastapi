from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas import UserResponse
from models import User

users_router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@users_router.get('', response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
