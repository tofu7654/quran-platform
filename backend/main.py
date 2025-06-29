from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.config import settings
from app.database import db_manager
from app.s3_audio import router as s3_audio_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Quran Platform API",
    description="A social media platform for sharing Quran recitations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")
app.include_router(s3_audio_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        db_manager.connect()
        logging.info("Application started successfully")
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    try:
        db_manager.disconnect()
        logging.info("Application shutdown successfully")
    except Exception as e:
        logging.error(f"Error during shutdown: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Quran Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.app_env == "development" else False
    ) 