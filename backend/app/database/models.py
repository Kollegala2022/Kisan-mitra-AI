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
    name = Column(String(100), nullable=True)
    language = Column(String(10), default="en")  # 'en' or 'kn'
    district = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")


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
