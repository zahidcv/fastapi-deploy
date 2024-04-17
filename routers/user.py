from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
# from database import SessionLocal, engine
from database import get_db
from routers.auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

user_dependency = Annotated[dict, Depends(get_current_user)]
pwd_cxt = CryptContext(schemes=['bcrypt'])

@router.post('/create', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/all", response_model=list[schemas.ShowUser])
def all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'No Blogs Found')
    return users


@router.get("/{id}", response_model=schemas.ShowUser)
def user(id, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.id == id).first()
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'{id} user not Found')
    return u


