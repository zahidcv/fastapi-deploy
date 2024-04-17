
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import database
import models
import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


router = APIRouter(
    tags=['Authentication']
)

pwd_cxt = CryptContext(schemes=['bcrypt'])
oauth2bearer = OAuth2PasswordBearer(tokenUrl='login')


@router.post('/login')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(database.get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    print(user)
    token = create_access_token(user.email, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}


def create_access_token(email: str, expires_delta: timedelta):
    expires = datetime.utcnow() + expires_delta
    encode = {'sub': email, 'exp': expires}
         
    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)

def authenticate_user(email, password, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect email')
    
    if not pwd_cxt.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Incorrect password')
    
    return user


def get_current_user(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get('sub')
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="couldn't validate user")
        return {'email': email}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTError, couldn't validate user")