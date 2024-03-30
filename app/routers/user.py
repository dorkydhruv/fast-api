from fastapi import status,HTTPException,Depends,APIRouter
from .. import schemas
from .. import models
from ..database import engine ,get_db
from ..utils import hashed
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#USER OPERATIONS
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):

    #hash the password
    user.password = hashed(user.password)

    #store the password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=404,detail=f"user with id {id} not found")