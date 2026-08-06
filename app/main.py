from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.users import Loginschema, SignupSchema, User
from app.database import get_db
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Wlecome to the App"}

@app.post("/login")
async def userlogin(user: Loginschema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.pwd != user.pwd:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "login successful", "user_id": db_user.id, "email": db_user.email}

@app.get("/admin/users")
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users


@app.post("/signup")
async def signupuser(newuser: SignupSchema, db: Session = Depends(get_db)):
    new_user = User(email=newuser.email, pwd= newuser.password, name = newuser.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user created", "id": new_user.id, "email": new_user.email}
    
    


