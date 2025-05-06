from passlib.context import CryptContext
from sqlalchemy import Column
import schemas
import models
from models import User
from database import Base, engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()


@app.post("/register")
def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = models.User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "user created successfully"}


@app.post('/login', response_model=schemas.TokenSchema)
def login(request: schemas.requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found, please register")
    hashed_pass = user.password
    if not pwd_context.verify(request.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    return {"access_token": user.email, "token_type": "you"}
