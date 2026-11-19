"""
Authentication routes for KisanMitra AI
Supports Sign Up, Login, Forgot Password (OTP via Mobile & Email link), Password Reset, and Session Management
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database.db import get_db
from app.database.models import User, AuthToken, PasswordReset

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


def generate_otp() -> str:
    """Generate a 6-digit numeric OTP"""
    return f"{secrets.randbelow(900000) + 100000}"


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
    email: Optional[str] = Field(None, max_length=150)
    district: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field("kn", max_length=10)


class LoginRequest(BaseModel):
    username: str  # Can be username, phone number, or email
    password: str


class ForgotPasswordRequest(BaseModel):
    channel: str = Field("mobile", pattern="^(mobile|email)$")  # 'mobile' or 'email'
    identifier: str  # Phone number or email address


class VerifyOtpRequest(BaseModel):
    identifier: str
    otp_code: str


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str = Field(..., min_length=4, max_length=100)


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class UserProfileResponse(BaseModel):
    id: int
    username: Optional[str]
    name: Optional[str]
    district: Optional[str]
    language: str
    phone: Optional[str]
    email: Optional[str]


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
    clean_email = req.email.strip().lower() if req.email else None
    clean_phone = req.phone.strip() if req.phone else None
    
    # Check if username already exists
    if db.query(User).filter(User.username == clean_username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken. Please choose another or login."
        )
        
    # Check if phone already registered
    if clean_phone and db.query(User).filter(User.phone == clean_phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This mobile number is already registered. Please login or reset password."
        )

    # Check if email already registered
    if clean_email and db.query(User).filter(User.email == clean_email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email address is already registered. Please login or reset password."
        )
    
    # Create user
    new_user = User(
        username=clean_username,
        email=clean_email,
        hashed_password=hash_password(req.password),
        name=req.name.strip() if req.name else clean_username,
        phone=clean_phone,
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
            phone=new_user.phone,
            email=new_user.email
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate farmer (by username, phone, or email) and return session token"""
    identifier = req.username.strip()
    identifier_lower = identifier.lower()
    
    # Search by username, phone, or email
    user = db.query(User).filter(
        or_(
            User.username == identifier_lower,
            User.phone == identifier,
            User.email == identifier_lower
        )
    ).first()
    
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/mobile or password. Please check and try again."
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
            phone=user.phone,
            email=user.email
        )
    )


@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Initiate password reset:
    - For mobile: generates a 6-digit OTP
    - For email: generates a reset code/link
    """
    clean_identifier = req.identifier.strip()
    
    if req.channel == "mobile":
        # Match phone (strip +91, spaces)
        clean_phone = clean_identifier.replace(" ", "").replace("-", "")
        if clean_phone.startswith("+91"):
            clean_phone = clean_phone[3:]
            
        user = db.query(User).filter(
            or_(
                User.phone == clean_identifier,
                User.phone == clean_phone,
                User.phone.like(f"%{clean_phone}%")
            )
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No farmer account found with this mobile number. Please check or register a new account."
            )
            
        otp = generate_otp()
        reset_token = generate_token()
        expires = datetime.utcnow() + timedelta(minutes=10)
        
        reset_entry = PasswordReset(
            user_id=user.id,
            channel="mobile",
            identifier=user.phone or clean_identifier,
            otp_code=otp,
            reset_token=reset_token,
            expires_at=expires,
            used=False
        )
        db.add(reset_entry)
        db.commit()
        
        print(f"==================================================")
        print(f"🌾 [OTP DISPATCH] Mobile: {clean_identifier} | OTP: {otp}")
        print(f"==================================================")
        
        return {
            "status": "success",
            "message": f"OTP successfully sent to mobile {clean_identifier}",
            "channel": "mobile",
            "identifier": clean_identifier,
            "otp_code": otp,  # Provided for immediate testing & demo
            "expires_in_minutes": 10
        }
        
    else:  # email
        clean_email = clean_identifier.lower()
        user = db.query(User).filter(User.email == clean_email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No account found with this email address."
            )
            
        otp = generate_otp()
        reset_token = generate_token()
        expires = datetime.utcnow() + timedelta(minutes=15)
        
        reset_entry = PasswordReset(
            user_id=user.id,
            channel="email",
            identifier=clean_email,
            otp_code=otp,
            reset_token=reset_token,
            expires_at=expires,
            used=False
        )
        db.add(reset_entry)
        db.commit()
        
        print(f"==================================================")
        print(f"🌾 [EMAIL RESET] To: {clean_email} | Reset Code: {otp} | Token: {reset_token}")
        print(f"==================================================")
        
        return {
            "status": "success",
            "message": f"Password reset instructions sent to {clean_email}",
            "channel": "email",
            "identifier": clean_email,
            "otp_code": otp,  # Provided for immediate testing & demo
            "reset_token": reset_token,
            "expires_in_minutes": 15
        }


@router.post("/verify-otp")
async def verify_otp(req: VerifyOtpRequest, db: Session = Depends(get_db)):
    """Verify the 6-digit OTP code submitted by the user"""
    clean_identifier = req.identifier.strip().lower()
    clean_otp = req.otp_code.strip()
    
    # Query latest active reset entry
    record = db.query(PasswordReset).filter(
        PasswordReset.otp_code == clean_otp,
        PasswordReset.used == False,
        PasswordReset.expires_at > datetime.utcnow()
    ).order_by(PasswordReset.created_at.desc()).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP. Please check the code or request a new one."
        )
        
    return {
        "status": "success",
        "message": "OTP verified successfully. You may now enter your new password.",
        "reset_token": record.reset_token
    }


@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Set new password using verified reset_token"""
    token_str = req.reset_token.strip()
    
    record = db.query(PasswordReset).filter(
        PasswordReset.reset_token == token_str,
        PasswordReset.used == False,
        PasswordReset.expires_at > datetime.utcnow()
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset session. Please request a new OTP."
        )
        
    user = record.user
    if not user:
        raise HTTPException(status_code=404, detail="User account not found.")
        
    # Update password
    user.hashed_password = hash_password(req.new_password)
    record.used = True
    
    # Invalidate existing active tokens to force re-login with new password
    db.query(AuthToken).filter(AuthToken.user_id == user.id).delete()
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Password updated successfully! Please login with your new password."
    }


@router.get("/me", response_model=UserProfileResponse)
async def get_me(user: User = Depends(require_current_user)):
    """Get current authenticated user profile"""
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        district=user.district,
        language=user.language or "kn",
        phone=user.phone,
        email=user.email
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
    """Update profile preferences (district, language, name, phone, email)"""
    if req.name is not None:
        user.name = req.name.strip()
    if req.district is not None:
        user.district = req.district.strip()
    if req.language and req.language in ["en", "kn"]:
        user.language = req.language
    if req.phone is not None:
        user.phone = req.phone.strip()
    if req.email is not None:
        user.email = req.email.strip().lower()
        
    db.commit()
    db.refresh(user)
    
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        district=user.district,
        language=user.language or "kn",
        phone=user.phone,
        email=user.email
    )
