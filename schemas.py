from typing import List
from pydantic import BaseModel, EmailStr


class TagBase(BaseModel):
    name: str


class TagResponse(TagBase):
    id: int


class TagCreate(TagBase):
    pass


class NoteBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    owner_id: int
    tags: List[TagResponse]

    class Config:
        orm_model = True


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
