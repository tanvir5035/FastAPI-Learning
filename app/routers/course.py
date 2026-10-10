from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session, session
from .. import models ,schema,utils      
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix="/course",
    tags=["Course"]
)

@router.post("/",response_model=schema.CourseResponse)
def create_course(course: schema.CourseCreate,db: Session = Depends(get_db),current_user:models.user = Depends(oauth2.get_current_user)):
    print(current_user.email)
    print(current_user.id)
    new_course =models.Course(
       **course.model_dump(),
       creator_id = current_user.id
    )
    new_course.website = str(new_course.website)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return  new_course




# @router.delete("/course/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_course(id:int):
#     cursor.execute("""delete from course where id= %s returning *""",(str(id)))
#     deleted_course = cursor.fetchone()
#     conn.commit()
#     if deleted_course == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"course with id {id} not found")
#     return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/",response_model=List[schema.CourseResponse])
def course(db:Session = Depends(get_db),current_user:models.user = Depends(oauth2.get_current_user),limit:int=5,skip:int=0,search:Optional[str] = ""):
    # course =db.query(models.Course).all()
    course =db.query(models.Course).filter(models.Course.creator_id == current_user.id).filter(models.Course.name.contains(search)).limit(limit).offset(skip).all()

    return course
   

@router.get("/{id}",response_model= schema.CourseResponse)
def course(id:int,db:Session = Depends(get_db),current_user:models.user = Depends(oauth2.get_current_user)):
    course =db.query(models.Course).filter(models.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"course with id {id} not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    return course
    #return {"status":"sqlalchemy is working"}


    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int,db:Session = Depends(get_db),current_user:models.user = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=404, detail=f"course with id {id} not found")   
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.CourseResponse)
def update_course(id:int,update_course:schema.CourseCreate,db:Session = Depends(get_db),current_user:models.user = Depends(oauth2.get_current_user)):
    course_query = db.query(models.Course).filter(models.Course.id == id)
    course = course_query.first()
    if not course:
        raise HTTPException(status_code=404, detail=f"course with id {id} not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    update_data = update_course.model_dump()
    update_data["website"] = str(update_data["website"])
    course_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(course)
    return  course