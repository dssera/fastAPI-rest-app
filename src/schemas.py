from typing import Union
from pydantic import BaseModel


class NoteBase(BaseModel):
    text: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    notes: list[Note] = []

    class Config:
        orm_mode = True