from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime, timezone
from app.database import Base
from pydantic import BaseModel

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(String)
    uploaded_by =  Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

class DocumentCreate(BaseModel):
    filename : str
    content : str