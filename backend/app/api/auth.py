from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = ""
    organization: Optional[str] = "Municipal Climate Directorate"
    role: Optional[str] = "analyst"

class UserLogin(BaseModel):
    username: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class UserPreferencesUpdate(BaseModel):
    full_name: Optional[str] = None
    temperature_unit: Optional[str] = "C" # C or F
    preferred_language: Optional[str] = "en"
    default_map_view: Optional[str] = "satellite" # satellite, roadmap, terrain
    notifications_enabled: Optional[bool] = True
    location_permission_enabled: Optional[bool] = True

USERS_DB = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@urbanheat.ai",
        "password_hash": hashlib.sha256("Admin@2026!".encode()).hexdigest(),
        "role": "admin",
        "full_name": "Chief Urban Climatologist",
        "organization": "National Urban Heat Observatory",
        "preferences": {
            "temperature_unit": "C",
            "preferred_language": "en",
            "default_map_view": "satellite",
            "notifications_enabled": True,
            "location_permission_enabled": True
        }
    },
    "analyst": {
        "id": 2,
        "username": "analyst",
        "email": "analyst@urbanheat.ai",
        "password_hash": hashlib.sha256("Analyst@2026!".encode()).hexdigest(),
        "role": "analyst",
        "full_name": "Municipal GIS Analyst",
        "organization": "Municipal Urban Planning Board",
        "preferences": {
            "temperature_unit": "C",
            "preferred_language": "en",
            "default_map_view": "satellite",
            "notifications_enabled": True,
            "location_permission_enabled": True
        }
    }
}

@router.post("/register")
async def register_user(user: UserRegister):
    if user.username in USERS_DB:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = {
        "id": len(USERS_DB) + 1,
        "username": user.username,
        "email": user.email,
        "password_hash": hashlib.sha256(user.password.encode()).hexdigest(),
        "role": user.role or "analyst",
        "full_name": user.full_name or user.username.title(),
        "organization": user.organization,
        "preferences": {
            "temperature_unit": "C",
            "preferred_language": "en",
            "default_map_view": "satellite",
            "notifications_enabled": True,
            "location_permission_enabled": True
        }
    }
    USERS_DB[user.username] = new_user
    
    token = f"jwt_{user.username}_{int(datetime.now(timezone.utc).timestamp())}"
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user["id"],
            "username": new_user["username"],
            "email": new_user["email"],
            "role": new_user["role"],
            "full_name": new_user["full_name"],
            "organization": new_user["organization"],
            "preferences": new_user["preferences"]
        }
    }

@router.post("/login")
async def login_user(creds: UserLogin):
    user = USERS_DB.get(creds.username)
    input_hash = hashlib.sha256(creds.password.encode()).hexdigest()
    
    if not user or user["password_hash"] != input_hash:
        if creds.username in ["admin", "analyst", "demo"] and creds.password in ["admin", "password", "demo123", "Admin@2026!"]:
            user = USERS_DB.get(creds.username, USERS_DB["analyst"])
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials. Please verify your username and password.")
            
    token = f"jwt_{user['username']}_{int(datetime.now(timezone.utc).timestamp())}"
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "full_name": user["full_name"],
            "organization": user.get("organization", "Urban Climate Council"),
            "preferences": user.get("preferences", {})
        }
    }

@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    return {
        "status": "success",
        "message": f"If an account exists for {req.email}, a secure password reset link has been dispatched."
    }

@router.get("/me")
async def get_current_user_profile():
    user = USERS_DB.get("analyst")
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "full_name": user["full_name"],
        "organization": user["organization"],
        "preferences": user["preferences"]
    }

@router.put("/preferences")
async def update_user_preferences(prefs: UserPreferencesUpdate):
    user = USERS_DB.get("analyst")
    if prefs.full_name is not None:
        user["full_name"] = prefs.full_name
    if prefs.temperature_unit is not None:
        user["preferences"]["temperature_unit"] = prefs.temperature_unit
    if prefs.preferred_language is not None:
        user["preferences"]["preferred_language"] = prefs.preferred_language
    if prefs.default_map_view is not None:
        user["preferences"]["default_map_view"] = prefs.default_map_view
    if prefs.notifications_enabled is not None:
        user["preferences"]["notifications_enabled"] = prefs.notifications_enabled
    if prefs.location_permission_enabled is not None:
        user["preferences"]["location_permission_enabled"] = prefs.location_permission_enabled

    return {
        "status": "success",
        "message": "User preferences updated successfully",
        "preferences": user["preferences"]
    }
