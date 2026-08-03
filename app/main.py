from fastapi import FastAPI
from app.models.users import Loginschema, SignupSchema
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Wlecome to the App"}

@app.post("/login")
async def userlogin(user: Loginschema):
    print("Details have been added")
    return{"UserID": user.email, "passwd": user.pwd}

@app.post("/signup")
async def signupuser(newuser: SignupSchema):
    print( f"new signup attemp by{newuser.email}")
    return{"message": "Signup Recieved", "email": newuser.email,
           "name": newuser.name}
    


