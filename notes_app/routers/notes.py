from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notes_app.database import get_db
from notes_app import models, schemas

notes_router = APIRouter(
    tags=['notes'],
    prefix='/notes'
)


@notes_router.get('', response_model=List[schemas.NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()


@notes_router.get('/{note_id}', response_model=schemas.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        return note
    raise HTTPException(status_code=404, detail='Not found')


@notes_router.post('', response_model=schemas.NoteResponse)
def post_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(**note.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@notes_router.put('/{note_id}', response_model=schemas.NoteResponse)
def update_note(note_id: int, updated_note: schemas.NoteCreate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        note.title = updated_note.title
        note.content = updated_note.content
        db.commit()
        db.refresh(note)
        return note
    raise HTTPException(status_code=404, detail='Not found')


@notes_router.delete('/{note_id}')
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
        return {'message': 'Note deleted'}
    raise HTTPException(status_code=404, detail='Not found')
