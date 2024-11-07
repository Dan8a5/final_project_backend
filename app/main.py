from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, parks
from app.config.config import engine
from sqlmodel import SQLModel

app = FastAPI(
    title="National Parks Explorer API",
    description="API for exploring US National Parks, creating itineraries, and getting park information",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
async def root():
    return {
        "message": "Welcome to the National Parks Explorer API",
        "documentation": "/docs",
        "endpoints": {
            "authentication": "/api/v1/auth",
            "parks": "/api/v1/parks",
            "version": "1.0.0"
        }
    }

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(parks.router, prefix="/api/v1")

# Initialize database
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)