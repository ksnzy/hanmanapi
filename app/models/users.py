from pydantic import BaseModel
from pydantic import EmailStr
from sqlalchemy import Column, Integer , String
from app.database import Base



class Loginschema(BaseModel):
    email: EmailStr
    pwd: str

class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    name: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index=True)
    email = Column(String, unique=True, index=True)
    pwd = Column(String)
    name = Column(String)
