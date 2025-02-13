from fastapi import Depends,HTTPException,APIRouter
from .. import oath2,models1,schema1 ,utils1
from sqlalchemy.orm import Session
from ..database1 import get_db
from ..protectionroutes import get_current_user
router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.put("/change-password")
def change_password(change_pass: schema1.ChangePassword, db: Session = Depends(get_db), current_user: models1.User = Depends(get_current_user)):
    user = db.query(models1.User).filter(models1.User.id == current_user["user_id"]).first()

    if not user or not utils1.verify_password(change_pass.old_password, user.password):
       
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.password = utils1.hash_password(change_pass.new_password)
    
    db.commit()

    return {"message": "Password changed successfully"}
