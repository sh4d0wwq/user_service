from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from ..db.database import Base

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    username: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserEdit(BaseModel):
    avatar_url: Optional[str] = None
    username: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    user_status: Optional[str] = None

    class Config:
        orm_mode = True

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    avatar_url = Column(String, unique=True)
    hashed_password = Column(String)
    user_status = Column(String)
    created_at = Column(String, default=func.now())