import sys
import os
import traceback
from pathlib import Path

# Initialize logging
print("Starting API initialization...")

# Add backend path
try:
    backend_path = Path(__file__).parent.parent / "backend"
    sys.path.insert(0, str(backend_path))
    print(f"Backend path added: {backend_path}")
except Exception as e:
    print(f"Error adding backend path: {e}")

# Create minimal FastAPI app first (fallback)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": "2026-04-28",
        "message": "AYF Connect API is running"
    }

@app.get("/api/")
async def root():
    return {
        "message": "AYF Connect API",
        "status": "running",
        "endpoints": [
            "/api/health",
            "/api/test"
        ]
    }

@app.get("/api/test")
async def test():
    return {"message": "Test endpoint working!"}

# Try to import your main app
try:
    print("Attempting to import main app...")
    from main import app as main_app
    
    # Copy routes from main app
    for route in main_app.routes:
        app.routes.append(route)
    print("Main app imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
    traceback.print_exc()
except Exception as e:
    print(f"Unexpected error: {e}")
    traceback.print_exc()

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    print(f"Global error: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )

# Vercel handler
handler = app
print("API initialized successfully!")
