from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteCreate):
    id: int
    owner_id: int

    class Config:
        orm_model = True
