from fastapi import APIRouter, Depends, HTTPException,status,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
import app.utils as utils
import app.schemas as schemas
import app.oauth as oauth

router = APIRouter(tags=['Auth'])

@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
          user = db.query(models.User).filter(models.User.email==user_credentials.username).first()

          if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
          
          if not utils.verify_password(user_credentials.password,user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
          
          #Create a new JWT token
          access_token = oauth.create_access_token(data={"user_id":user.id})
          return {"access_token":access_token,"token_type":"bearer"}