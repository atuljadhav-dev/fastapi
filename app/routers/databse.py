from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.dependencies.get_db import get_mongodb, get_sqldb, User
from pydantic import BaseModel


# from app.schemas.User import User as user
class Users(BaseModel):
    id: int
    name: str


router = APIRouter(
    prefix="/database",
    tags=["Database"],
)


@router.get("/sql/users", tags=["SQL"])
def users(db: Session = Depends(get_sqldb)):
    """Get all users from the database"""
    return db.query(User).all()


@router.post("/sql/users", tags=["SQL"])
def add(user: Users, db: Session = Depends(get_sqldb)):
    """Add a new user to the database"""
    try:
        user = User(name=user.name, id=user.id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        return e


@router.get("/sql/users/{user_id}", tags=["SQL"])
def get_user(user_id: int, db: Session = Depends(get_sqldb)):
    """Get a user by ID from the database"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        return {"message": "User not found"}


@router.put("/sql/users/{user_id}", tags=["SQL"])
def update_user(user_id: int, user: Users, db: Session = Depends(get_sqldb)):
    """Update a user by ID in the database"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return {"message": "User not found"}


@router.delete("/sql/users/{user_id}", tags=["SQL"])
def delete_user(user_id: int, db: Session = Depends(get_sqldb)):
    """Delete a user by ID from the database"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}


# MongoDB routes
@router.get("/mongodb/users", tags=["MongoDB"])
def get_mongodb_users(users=Depends(get_mongodb)):
    """Get all users from the MongoDB database"""
    return list(users.find({}, {"_id": 0}))


@router.post("/mongodb/users", tags=["MongoDB"])
def add_mongodb_user(user: Users, users=Depends(get_mongodb)):
    """Add a new user to the MongoDB database"""
    user_dict = user.dict()
    users.insert_one(user_dict)
    return user



@router.get("/mongodb/users/{user_id}", tags=["MongoDB"])
def get_mongodb_user(user_id: int, users=Depends(get_mongodb)):
    """Get a user by ID from the MongoDB database"""
    user = users.find_one({"id": user_id}, {"_id": 0})
    if user:
        return user
    else:
        return {"message": "User not found"}



@router.put("/mongodb/users/{user_id}", tags=["MongoDB"])
def update_mongodb_user(user_id: int, user: Users, users=Depends(get_mongodb)):
    """Update a user by ID in the MongoDB database"""
    result = users.update_one({"id": user_id}, {"$set": user.dict()})
    if result.modified_count:
        return {"message": "User updated successfully"}
    else:
        return {"message": "User not found"}


@router.delete("/mongodb/users/{user_id}", tags=["MongoDB"])
def delete_mongodb_user(user_id: int, users=Depends(get_mongodb)):
    """Delete a user by ID from the MongoDB database"""
    result = users.delete_one({"id": user_id})
    if result.deleted_count:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}
