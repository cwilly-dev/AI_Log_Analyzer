from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.database.db import get_db
from app.schemas.user import UserOut
from app.api.deps import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/all_users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    result = db.execute(select(User).order_by(User.email))
    users = result.scalars().all()
    return users

@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user