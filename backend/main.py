from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
from routes import auth, calendar, quarterly, chat, feed, profile, admin
from database import supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("AYF Connect API Starting...")
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="AYF Connect API",
    description="API for AYF Gwarimpa Archdeaconry Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://ayf-connect.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Include routers
app.include_router(auth.router)
app.include_router(calendar.router)
app.include_router(quarterly.router)
app.include_router(chat.router)
app.include_router(feed.router)
app.include_router(profile.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {"message": "AYF Connect API", "status": "running"}

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        supabase.table("users").select("count").limit(1).execute()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
