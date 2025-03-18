from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from utils.auth import get_current_user
from database.database import get_db
from models import Tag, User, Note
from schemas import NoteResponse, NoteCreate
from utils.tags import process_tags

notes_router = APIRouter(
    tags=['notes'],
    prefix='/notes'
)


@notes_router.get('', response_model=List[NoteResponse])
def get_notes(
    tag: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Note).filter(
        Note.owner_id == current_user.id)

    if tag:
        query = query.join(Note.tags).filter(Tag.name == tag)

    return query.all()


@notes_router.get("/search", response_model=List[NoteResponse])
def search_notes(
    query: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notes = db.query(Note).filter(
        Note.owner_id == current_user.id,
        or_(
            Note.title.ilike(f"%{query}%"),
            Note.content.ilike(f"%{query}%"),
            Note.tags.any(Tag.name.ilike(f"%{query}%"))
        )
    ).offset(skip).limit(limit).all()

    if not notes:
        raise HTTPException(status_code=404, detail="No notes found")

    return notes


@notes_router.get('/{note_id}', response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user:
        note = db.query(Note).filter(
            (Note.id == note_id) & (Note.owner_id == current_user.id)).first()
    if note:
        return note
    raise HTTPException(status_code=404, detail='Not found')


@notes_router.post('', response_model=NoteResponse)
def post_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    tags = process_tags(db, note.tags)
    note.tags = process_tags(db, note.tags)
    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id,
        tags=tags
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@notes_router.put('/{note_id}', response_model=NoteResponse)
def update_note(
    note_id: int,
    updated_note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        (Note.id == note_id) & (Note.owner_id == current_user.id)).first()
    if note:
        note.title = updated_note.title
        note.content = updated_note.content
        db.commit()
        db.refresh(note)
        return note
    raise HTTPException(status_code=404, detail='Not found')


@notes_router.delete('/{note_id}')
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        (Note.id == note_id) & (Note.owner_id == current_user.id)).first()
    if note:
        db.delete(note)
        db.commit()
        return {'message': 'Note deleted'}
    raise HTTPException(status_code=404, detail='Not found')
