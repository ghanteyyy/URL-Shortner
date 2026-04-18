import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from .schemas import UserCreate, UserOut
from .models import User

router = APIRouter()


@router.post("/register", response_model=UserOut)
def create_user(user: UserCreate = Depends(UserCreate.as_form), db: Session = Depends(get_db)):
    if db.query(User).exists(User.email == user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    db_user = User(name=user.name, email=user.email, gender=user.gender, dob=user.dob)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.delete("/user/{id}")
def delete_user(id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
