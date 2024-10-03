from typing import Annotated

import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from src import models, schemas, crud
from src.database import engine, SessionLocal
from src.schemas import UserCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Session = Depends(get_db)):
    # it's called when user try to login
    # user_dict = fake_users_db.get(form_data.username)
    user: models.User = crud.get_user_by_username(db=db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict),
    user_ = UserCreate(username=user.username, password=user.hashed_password) # actually not hashed
    if not form_data.password == user_.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


def fake_decode_token(token, db: Session = Depends(get_db)):
    # This doesn't provide any security at all
    # Check the next version
    # token is username actually
    user = crud.get_user_by_username(db=db, username=token)
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/notes/", response_model=schemas.User)
def create_note(note: schemas.NoteCreate,
                user: Annotated[schemas.User, get_current_user],
                db: Session = Depends(get_db)):
    # probably a place for Яндекс.Спеллер validation
    # to get owner_id we need to implement auth system
    current_user_id = user.id
    print(current_user_id)
    return crud.create_note(db=db, note=note, owner_id=current_user_id)


@app.get("/notes/", response_model=list[schemas.Note]) #
def read_notes(token: Annotated[str, Depends(oauth2_scheme)],
               skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_db)):
    notes = crud.get_note(db=db, skip=skip, limit=limit)
    return notes


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)