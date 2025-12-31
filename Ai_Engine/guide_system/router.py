from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Ensure parent directory is in path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import models
from database import get_db

router = APIRouter(prefix="/guide", tags=["Guide System"])

class GuideSignup(BaseModel):
    full_name: str
    email: str
    password: str
    primary_domain: str
    years_experience: int
    current_role: str
    organization: str
    linkedin_portfolio_url: str
    bio: str
    weekly_availability: str

class GuideLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register_guide(data: GuideSignup, db: Session = Depends(get_db)):
    # Check existing user
    existing_user = db.query(models.User).filter(models.User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    try:
        # Create Base User
        user = models.User(
            name=data.full_name,
            email=data.email,
            password=data.password,
            username=data.email, # Use email as username for uniqueness
            role="guide"
        )
        db.add(user)
        db.flush() # Get user ID
        
        # Create Independent Guide Record
        guide = models.Guide(
            user_id=user.id,
            full_name=data.full_name,
            email=data.email,
            password=data.password,
            primary_domain=data.primary_domain,
            years_experience=data.years_experience,
            current_role=data.current_role,
            organization=data.organization,
            linkedin_portfolio_url=data.linkedin_portfolio_url,
            bio=data.bio,
            weekly_availability=data.weekly_availability,
            verified=False
        )
        db.add(guide)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Guide registration failed: {str(e)}")
    
    return {"message": "Guide account created successfully. Awaiting verification."}

@router.post("/auth/login")
async def login_guide(data: GuideLogin, db: Session = Depends(get_db)):
    guide = db.query(models.Guide).filter(models.Guide.email == data.email).first()
    if not guide or guide.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials for Guide account")
    
    return {
        "message": "Login successful",
        "guide": {
            "id": guide.user_id,
            "name": guide.full_name,
            "email": guide.email,
            "verified": guide.verified,
            "role": "guide"
        }
    }
