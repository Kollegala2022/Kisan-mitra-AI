"""
Database models for KisanMitra AI
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True, nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    name = Column(String(100), nullable=True)
    phone = Column(String(20), index=True, nullable=True)
    language = Column(String(10), default="en")  # 'en' or 'kn'
    district = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")


class AuthToken(Base):
    __tablename__ = "auth_tokens"
    
    id = Column(Integer, primary_key=True)
    token = Column(String(128), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tokens")


class PasswordReset(Base):
    __tablename__ = "password_resets"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel = Column(String(20), nullable=False)  # 'mobile' or 'email'
    identifier = Column(String(150), nullable=False)  # phone number or email address
    otp_code = Column(String(10), nullable=True)  # 6-digit OTP code
    reset_token = Column(String(128), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="password_resets")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    farmer_context = relationship("FarmerContext", back_populates="conversation", uselist=False, cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sources = Column(Text, nullable=True)  # JSON string of sources
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class FarmerContext(Base):
    __tablename__ = "farmer_context"
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, unique=True)
    district = Column(String(100), nullable=True)
    taluk = Column(String(100), nullable=True)
    crop = Column(String(100), nullable=True)
    soil_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="farmer_context")


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    topic = Column(String(100), nullable=False)  # 'crop', 'soil', 'irrigation', 'pest', 'disease', 'scheme', 'general'
    crop = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)
    source_name = Column(String(200), nullable=True)
    source_url = Column(String(500), nullable=True)
    reviewed_date = Column(DateTime, nullable=True)
    language = Column(String(10), default="en")  # 'en' or 'kn'
    created_at = Column(DateTime, default=datetime.utcnow)


class SchemeLink(Base):
    __tablename__ = "scheme_links"
    
    id = Column(Integer, primary_key=True)
    scheme_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    eligibility = Column(Text, nullable=True)
    official_url = Column(String(500), nullable=False)
    reviewed_date = Column(DateTime, nullable=True)
    language = Column(String(10), default="en")  # 'en' or 'kn'
    created_at = Column(DateTime, default=datetime.utcnow)
