from .database import Base, SessionLocal, engine
from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column("hashed_password", String, nullable=False)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

    # 🔹 This is the user_id field
    user_id = Column(Integer, ForeignKey("users.id"))

    # relationship
    user = relationship("User", back_populates="tasks")

