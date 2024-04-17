from typing import Annotated


from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
# from database import SessionLocal, engine
from database import get_db
import routers.auth as auth


router = APIRouter(
    tags=['blogs'],
    prefix="/blog"
)
user_dependency = Annotated[dict, Depends(auth.get_current_user)]


@router.post('/create', status_code=status.HTTP_201_CREATED, )
def create_blog(request:schemas.Blog, current_user: user_dependency, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@router.get("/all", response_model=list[schemas.ShowBlog], )
def blogs(current_user: user_dependency, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'No Blogs Found')
    return blogs

@router.get("/{id}", response_model=schemas.ShowBlog, )
def blog(id,current_user: user_dependency, db: Session = Depends(get_db)):
    b = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'{id} blog not Found')
    return b

@router.delete('/delete/{id}', )
def delete(id, current_user: user_dependency, db: Session = Depends(get_db)):
    b = db.query(models.Blog).filter(models.Blog.id == id)
    if not b.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id}Blog not found')
    b.delete()
    db.commit()
    return 'deleted'

@router.put('/update/{id}', )
def update(id, current_user: user_dependency, request: schemas.Blog, db: Session = Depends(get_db)):
    b = db.query(models.Blog).filter(models.Blog.id == id)
    if not b.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id}Blog not found')
    b.update(dict(request))
    db.commit()
    return 'updated'