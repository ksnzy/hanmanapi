from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models.users import Loginschema, SignupSchema, User
from app.database import get_db
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Wlecome to the App"}

@app.post("/login")
async def userlogin(user: Loginschema):
    print("Details have been added")
    return{"UserID": user.email, "passwd": user.pwd}

@app.post("/signup")
async def signupuser(newuser: SignupSchema, db: Session = Depends(get_db)):
    new_user = User(email=newuser.email, pwd= newuser.password, name = newuser.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user created", "id": new_user.id, "email": new_user.email}
    
    


