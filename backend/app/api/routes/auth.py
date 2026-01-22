from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.database.db import get_db
from app.schemas.user import UserCreate, UserOut, UserLogin
from app.core.security import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login-json")
def login_json(
        payload: UserLogin,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials",
        )
    token = create_access_token({"sub": str(user.id)}, 60)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials",
        )
    token = create_access_token({"sub": str(user.id)}, 60)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
def register(
        user_in:UserCreate,
        db: Session = Depends(get_db)
):
    user =  User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )

    existing = db.query(User).filter(User.email == user_in.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db.add(user)
    db.commit()
    return user