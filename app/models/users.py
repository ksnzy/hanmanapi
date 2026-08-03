from pydantic import BaseModel
from pydantic import EmailStr

class Loginschema(BaseModel):
    email: EmailStr
    pwd: str

class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    name: str