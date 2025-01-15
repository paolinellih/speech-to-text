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

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str
    class Config:
        orm_mode = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True
