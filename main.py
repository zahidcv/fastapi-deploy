from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine, get_db
from routers import auth, blog, user
from schemas import Blog

app = FastAPI()

models.Base.metadata.create_all(engine) 

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/', tags=['root'])
def hello():
    return {'message': 'Hello from Zahid'}
 