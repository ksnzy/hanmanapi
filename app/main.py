from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.users import Loginschema, SignupSchema, User
from app.database import get_db
from app.hashing import verify_password, hash_password
from app.auth import create_access_token, get_current_user
from app.models.documents import Document , DocumentCreate, Chunk
from app.embeddings import get_embedding, chunk_text
import json




app = FastAPI()


@app.post("/login")
async def userlogin(user: Loginschema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.pwd, db_user.pwd):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data = {"user_id": db_user.id, "email": db_user.email})

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/admin/users")
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return all_users


@app.post("/signup")
async def signupuser(newuser: SignupSchema, db: Session = Depends(get_db)):
    new_user = User(email=newuser.email, pwd= hash_password(newuser.password), name = newuser.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "user created", "id": new_user.id, "email": new_user.email}



@app.post("/documents")
async def upload_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_doc = Document(
        filename=doc.filename,
        content=doc.content,
        uploaded_by=current_user["user_id"]
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    text_chunks = chunk_text(doc.content)
    for chunk_str in text_chunks:
        vector = get_embedding(chunk_str)
        new_chunk = Chunk(
            document_id=new_doc.id,
            text=chunk_str,
            embedding=json.dumps(vector)
        )
        db.add(new_chunk)
    db.commit()

    return {"message": "document uploaded and embedded", "id": new_doc.id, "chunks_created": len(text_chunks)}


@app.get("/all_documents")
def get_all_documents(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    all_docs = db.query(Document).filter(Document.is_active == True).all()
    return all_docs
    
    


