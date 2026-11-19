"""
Authentication routes for KisanMitra AI
Supports Sign Up, Login, Current User verification, and Logout
"""
import hashlib
import secrets
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User, AuthToken

router = APIRouter(prefix="/api/auth", tags=["auth"])


# --- Password & Token Security Utilities ---

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with 100k rounds and salt"""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${key}"


def verify_password(plain_password: str, stored_hash: Optional[str]) -> bool:
    """Verify password against stored salt$key hash"""
    if not stored_hash or "$" not in stored_hash:
        return False
    try:
        salt, _ = stored_hash.split("$", 1)
        expected = hash_password(plain_password, salt)
        return secrets.compare_digest(stored_hash, expected)
    except Exception:
        return False


def generate_token() -> str:
    """Generate a high-entropy 256-bit authentication token"""
    return secrets.token_hex(32)


def get_current_user_from_token(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Dependency helper to get current authenticated user if token is present"""
    if not authorization:
        return None
    
    token = authorization
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    
    if not token:
        return None
    
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).first()
    if auth_token:
        return auth_token.user
    return None


def require_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Dependency enforcing authentication"""
    user = get_current_user_from_token(authorization, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in."
        )
    return user


# --- Schemas ---

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=100)
    name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    district: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field("kn", max_length=10)


class LoginRequest(BaseModel):
    username: str
    password: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = None
    phone: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    username: Optional[str]
    name: Optional[str]
    district: Optional[str]
    language: str
    phone: Optional[str]


class AuthResponse(BaseModel):
    status: str
    message: str
    token: str
    user: UserProfileResponse


# --- Endpoints ---

@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignupRequest, db: Session = Depends(get_db)):
    """Register a new farmer account"""
    clean_username = req.username.strip().lower()
    
    # Check if username already exists
    existing = db.query(User).filter(User.username == clean_username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or mobile number is already registered. Please login."
        )
    
    # Create user
    new_user = User(
        username=clean_username,
        hashed_password=hash_password(req.password),
        name=req.name.strip() if req.name else clean_username,
        phone=req.phone.strip() if req.phone else None,
        district=req.district.strip() if req.district else None,
        language=req.language if req.language in ["en", "kn"] else "kn"
    )
    db.add(new_user)
    db.flush()
    
    # Issue auth token
    token_str = generate_token()
    token_record = AuthToken(token=token_str, user_id=new_user.id)
    db.add(token_record)
    db.commit()
    db.refresh(new_user)
    
    return AuthResponse(
        status="success",
        message="Account registered successfully",
        token=token_str,
        user=UserProfileResponse(
            id=new_user.id,
            username=new_user.username,
            name=new_user.name,
            district=new_user.district,
            language=new_user.language or "kn",
            phone=new_user.phone
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate farmer and return session token"""
    clean_username = req.username.strip().lower()
    
    user = db.query(User).filter(User.username == clean_username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Issue auth token
    token_str = generate_token()
    token_record = AuthToken(token=token_str, user_id=user.id)
    db.add(token_record)
    db.commit()
    
    return AuthResponse(
        status="success",
        message="Login successful",
        token=token_str,
        user=UserProfileResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            district=user.district,
            language=user.language or "kn",
            phone=user.phone
        )
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_me(user: User = Depends(require_current_user)):
    """Get current authenticated user profile"""
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        district=user.district,
        language=user.language or "kn",
        phone=user.phone
    )


@router.post("/logout")
async def logout(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Log out by invalidating active session token"""
    if authorization:
        token = authorization
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
        if token:
            db.query(AuthToken).filter(AuthToken.token == token).delete()
            db.commit()
            
    return {"status": "success", "message": "Logged out successfully"}


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    req: UpdateProfileRequest,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """Update profile preferences (district, language, name)"""
    if req.name is not None:
        user.name = req.name.strip()
    if req.district is not None:
        user.district = req.district.strip()
    if req.language and req.language in ["en", "kn"]:
        user.language = req.language
    if req.phone is not None:
        user.phone = req.phone.strip()
        
    db.commit()
    db.refresh(user)
    
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        district=user.district,
        language=user.language or "kn",
        phone=user.phone
    )
