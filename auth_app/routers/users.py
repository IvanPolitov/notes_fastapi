from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db

from auth_app import schemas
from auth_app import models

users_router = APIRouter(
    tags=['users'],
    prefix='/users'
)


@users_router.get('', response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()
