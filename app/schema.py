from pydantic import BaseModel, HttpUrl,EmailStr
from datetime import datetime
from typing import Optional
class CourseCreate(BaseModel): 
    name: str
    instructor: str
    course_duration: float
    website: HttpUrl

class CourseResponse(CourseCreate):
    id : int
    creator_id: int

    class Config:
        orm_mode = True
        
# class CourseResponse(BaseModel):
#    id: int
#    name: str
#    instructor: str
#    course_duration: float
#    website: HttpUrl
#    class Config:
#        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    email:str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id : int 
   