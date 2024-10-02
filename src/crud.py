from typing import List, Type

from sqlalchemy.orm import Session

from . import models
from . import schemas


def get_notes(db: Session, skip: int = 0, limit: int = 100) -> List[Type[models.Note]]:
    return db.query(models.Note).offset(skip).limit(limit).all()


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def create_note(db: Session, note: schemas.NoteCreate, owner_id) -> models.Note:
    db_note = models.Note(text=note.text, owner_id=owner_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Type[models.Note]]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()