"""from sqlalchemy import DateTime, Float, Integer, Column, String, column, false,String


from math import integer
from .database import Base

class Course(Base):
    __tablename__ = "courses"
    id = column(integer, primary_key=True, index=True)
    name = column(String, nullable= false)
    instructor = column(String, nullable= false)
    course_duration = column(Float, nullable= false)
    website = column(String,nullable= false)"""
"""from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    course_duration = Column(Float, nullable=False)
    website = Column(String, nullable=False)"""
from sqlalchemy import Column, Integer, String, Float,TIMESTAMP, false,text,ForeignKey

from .database import Base


class Course(Base):
    __tablename__ = "course"          
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    course_duration = Column(Float, nullable=False)
    website = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)



class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone= True),nullable = false,server_default=text('now()'))