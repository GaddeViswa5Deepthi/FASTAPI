
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import null,func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base



class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published= Column(Boolean,server_default="True",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"),nullable=False)
    owner=relationship("User")



class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="cascade"),primary_key=True)