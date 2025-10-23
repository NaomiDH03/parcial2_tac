from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User
from schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    new_user = User(name=user.name, balance=user.balance)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
