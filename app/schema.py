
from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published:bool = True
class PostCreate(PostBase)  :
    pass  
class userout(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True
class Posts(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:userout
    class Config:
        orm_mode=True
class usercreate(BaseModel):
    email:EmailStr
    password:str
    class Config:
        orm_mode=True
# class userout(BaseModel):
#     id:int
#     email:EmailStr
#     created_at:datetime
#     class Config:
#         orm_mode=True

class UserLogin(BaseModel):
    email:EmailStr
    password:str
class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[str]=None
class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1)
class Postout(PostBase):
    Post:dict
    votes:int
    class Config:
        orm_mode=True