from .. import models,schema,utils
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

router=APIRouter(
    prefix="/users",
    tags=["USERS"]
   
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.userout)
def create_user(user:schema.usercreate,db:Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password= hashed_password
    new_user = models.User(**user.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
     
    return new_user
@router.get("/{id}",status_code=status.HTTP_201_CREATED,response_model=schema.userout)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} desnot exist")
    return user