from pydantic import BaseModel
import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# class TokenSchema(BaseModel):
#     email: str
#     password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class requestdetails(BaseModel):
    email: str
    password: str
