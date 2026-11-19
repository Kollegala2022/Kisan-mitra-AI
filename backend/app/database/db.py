"""
Database connection and session management
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from .models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kisanmitra.db")

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables and run lightweight migrations"""
    Base.metadata.create_all(bind=engine)
    
    # Safe migration for existing SQLite database
    if "sqlite" in DATABASE_URL:
        try:
            with engine.connect() as conn:
                res = conn.execute(text("PRAGMA table_info(users)"))
                cols = [row[1] for row in res.fetchall()]
                if "username" not in cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(100)"))
                if "hashed_password" not in cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR(255)"))
                if "phone" not in cols:
                    conn.execute(text("ALTER TABLE users ADD COLUMN phone VARCHAR(20)"))
                conn.commit()
        except Exception as e:
            print(f"Warning during migration: {e}")
            
    print("Database tables created and updated successfully")
