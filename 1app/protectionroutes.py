from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models1, oath2, database1

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database1.get_db)):
    payload = oath2.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(models1.User).filter(models1.User.id == payload["user_id"]).first()
    return {"user_id": user.id, "email": user.email}
