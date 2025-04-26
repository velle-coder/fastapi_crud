from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/dev_crud"
engine = create_engine(DATABASE_URL)
session = Session(engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel
app = FastAPI()

class UserBase(BaseModel):
    name: str
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    print("-------")
    db_user = User(**user.model_dump())
    print(db_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100):
    users = session.query(User).offset(skip).limit(limit).all()
    return users
#
# @app.get("/users/{user_id}", response_model=User)
# def read_user(user_id: int):
#     user = session.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, user: UserBase):
#     db_user = session.query(User).filter(User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     for key, value in user.dict().items():
#         setattr(db_user, key, value)
#     session.commit()
#     session.refresh(db_user)
#     return db_user
#
# @app.delete("/users/{user_id}", response_model=User)
# def delete_user(user_id: int):
#     user = session.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     session.delete(user)
#     session.commit()
#     return user


