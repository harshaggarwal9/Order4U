from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db.session import SessionLocal
from app.models.user import users
from app.schema.user import UserCreate, UserLogin, UserUpdate
from app.core.security import create_access_token
from app.core.security import get_current_user
from app.db.session import get_db
from app.core.security import hash_password, verify_password

router = APIRouter( tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
def register(payload: UserCreate, db: Session = Depends(get_db)):
   
    if db.query(users).filter(users.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(users).filter(users.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = users(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    
    user = db.query(users).filter(users.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
        

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.put("/me", status_code=status.HTTP_200_OK)
def update_profile(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Update username if provided
    if payload.username is not None:
        current_user.username = payload.username

    # Update email if provided
    if payload.email is not None:
        current_user.email = payload.email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    }
