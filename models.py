from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


note_tag_association = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    tags: Mapped[List['Tag']] = relationship(
        secondary=note_tag_association, back_populates='notes')
    owner: Mapped["User"] = relationship(back_populates="notes")


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped["Note"] = relationship(back_populates="owner")


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    notes: Mapped[List["Note"]] = relationship(
        secondary=note_tag_association, back_populates='tags')
