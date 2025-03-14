from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped["Note"] = relationship(back_populates="owner")
