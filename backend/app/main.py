"""
FastAPI application main file
"""
import os
from dotenv import load_dotenv

# Load environment variables FIRST, before any other imports
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try to import GZIPMiddleware, but don't fail if unavailable
try:
    from starlette.middleware.gzip import GZIPMiddleware
except ImportError:
    GZIPMiddleware = None

from app.database.db import init_db
from app.rag.ingest import seed_initial_knowledge_base, add_knowledge_documents_to_rag
from app.database.db import SessionLocal
from app.routes import chat, reference

# Create FastAPI app
app = FastAPI(
    title="KisanMitra AI",
    description="AI-powered farmer assistance chatbot for Karnataka",
    version="0.1.0"
)

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP middleware if available
if GZIPMiddleware:
    app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Include routers
app.include_router(chat.router)
app.include_router(reference.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup"""
    try:
        print("Initializing database...")
        init_db()
        
        # Seed knowledge base
        db = SessionLocal()
        try:
            seed_initial_knowledge_base(db)
            add_knowledge_documents_to_rag(db)
            print("Knowledge base initialized successfully")
        finally:
            db.close()
        
        print("✓ KisanMitra AI backend started successfully")
    except Exception as e:
        print(f"✗ Startup error: {e}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "KisanMitra AI",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "KisanMitra AI",
        "description": "AI-powered farmer assistance chatbot for Karnataka",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "conversations": "/api/conversations",
            "crops": "/api/crops",
            "districts": "/api/districts",
            "schemes": "/api/schemes",
            "weather": "/api/weather"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
