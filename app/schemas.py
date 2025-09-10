from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

# JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# 🔹 Base schema for common task fields
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


# 🔹 Schema for creating a new task
class TaskCreate(TaskBase):
    pass  # inherits title and description from TaskBase


# 🔹 Schema for returning a task (includes id and user_id)
class Task(TaskBase):
    id: int
    user_id: int  # link to the owner

    class Config:
        orm_mode = True  # tells Pydantic to read data from ORM models
