from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from app.models.user import User
from app.dependencies import get_db
from app.config.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        # Create user in Supabase
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        # Create user in our database
        db_user = User(
            id=auth_response.user.id,
            email=user_data.email,
            full_name=user_data.full_name
        )
        db.add(db_user)
        db.commit()
        
        return {
            "message": "User created successfully",
            "access_token": auth_response.session.access_token,
            "user": {
                "email": user_data.email,
                "full_name": user_data.full_name
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/login")
async def login(credentials: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        return {
            "access_token": response.session.access_token,
            "user": {
                "email": credentials.email
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

@router.post("/logout")
async def logout(token: str = Depends(get_db)):
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Error logging out"
        )

# Simple endpoint to demonstrate authentication
@router.get("/protected")
async def protected_route(token: str = Depends(get_db)):
    try:
        user = supabase.auth.get_user(token)
        return {"message": f"Hello {user.user.email}! This is a protected route."}
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )