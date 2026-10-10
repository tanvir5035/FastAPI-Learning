from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import session,Session
from .. import models ,schema         
from ..database import get_db
from .. import utils             

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/",response_model = schema.UserResponse)
def create_user(user:schema.UserCreate,db:session = Depends(get_db)):
    if db.query(models.user).filter(models.user.email == user.email).first():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exists")
    hash_password = utils.hash_password(user.password)
    user.password = hash_password
    new_user = models.user(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model = schema.UserResponse)
def get_user(id:int,db:session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id ==id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.get("/",response_model=List[schema.UserResponse])
def user_(db:session = Depends(get_db)):
    user =db.query(models.user).all()
    return user
   