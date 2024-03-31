from jose import JWTError,jwt
from datetime import datetime, timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas
from . import database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET KEY
#ALGORITHM
#EXPIRATION TIME

SECRET_KEY= "bedd24304977cb9e4d47e4e3f1b4036a7fe8b24b78e5d5291bf8337657a19949"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode =data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def access_token(token:str,credentials_exception):
    try:
        payload =jwt.decode(token,SECRET_KEY,[ALGORITHM])
        id =payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token = access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user