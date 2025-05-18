from app.schemas.base import NoWhitespaceString
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: NoWhitespaceString


class UserCreate(UserBase):
    password: NoWhitespaceString


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: EmailStr | NoWhitespaceString
    password: NoWhitespaceString
