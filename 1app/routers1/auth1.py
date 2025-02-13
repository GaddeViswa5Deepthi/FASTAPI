from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database1 import get_db
from .. import models1, schema1 , utils1,oath2
from ..protectionroutes import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schema1.UserResponse)
def register_user(user_data: schema1.UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user = db.query(models1.User).filter(models1.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and create the user
    hashed_password = utils1.hash_password(user_data.password)
    
    new_user = models1.User(name=user_data.name, email=user_data.email, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
@router.put("/change-password")
def change_password(change_pass: schema1.ChangePassword, db: Session = Depends(get_db), current_user: models1.User = Depends(get_current_user)):
    user = db.query(models1.User).filter(models1.User.id == current_user["user_id"]).first()

    if not user or not utils1.verify_password(change_pass.old_password, user.password):
       
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.password = utils1.hash_password(change_pass.new_password)
    
    db.commit()

    return {"message": "Password changed successfully"}
@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models1.User).filter(models1.User.email == form_data.username).first()

    if not user or not utils1.verify_password(form_data.password, user.password):
  
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = oath2.create_access_token({"user_id": user.id})
    
    return {"access_token": token, "token_type": "bearer"}