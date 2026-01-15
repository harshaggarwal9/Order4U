from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(min_length=3,max_length=50,description="Unique username")
    email: EmailStr = Field(description="User email address")
    password: str = Field(min_length=6,description="User password (plain text, will be hashed)")

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None,min_length=3,max_length=50,description="Updated username")
    email: Optional[EmailStr] = Field(default=None,description="Updated email address")


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
