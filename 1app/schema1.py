from pydantic import BaseModel, EmailStr

# User registration schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # Raw password

# User response schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# Change password schema
class ChangePassword(BaseModel):
    old_password: str
    new_password: str