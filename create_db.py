from app.database import Base, engine
from app.models.users import User
from app.models.documents import Document, Chunk

Base.metadata.create_all(bind=engine)
print("Database and tables created.")