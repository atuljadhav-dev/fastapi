from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_sqldb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy import Column, Integer, String,Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    # email = Column(String(50), unique=True, index=True)
    # password = Column(String(50))
    # is_active = Column(Boolean, default=True)
    # created_at = Column(DateTime)


Base.metadata.create_all(bind=engine)


from pymongo import MongoClient
client = MongoClient(
    "mongodb://localhost:27017"
)
db = client["mydatabase"] 
users = db["users"]

def get_mongodb():
    return users