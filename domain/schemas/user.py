from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True