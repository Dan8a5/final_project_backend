from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes.parks import router as parks_router
from app.routes.itineraries import itineraries_router  # Import itineraries router
from app.config.config import engine
from sqlmodel import SQLModel

app = FastAPI(
    title="National Parks Explorer API",
    description="API for exploring US National Parks, creating itineraries, and getting park information",
    version="1.0.0"
)

async def lifespan(app: FastAPI):
    # This is where you can initialize resources
    # (e.g., creating tables or connecting to databases)
    SQLModel.metadata.create_all(engine)
    
    yield  # This is where FastAPI will pause until the app is shutting down

    # This is where you can clean up resources
    # (e.g., closing database connections)

app.lifespan = lifespan

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
            "itineraries": "/api/v1/itineraries",  # Add itineraries endpoint reference
            "version": "1.0.0"
        }
    }

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(parks_router, prefix="/api/v1")
app.include_router(itineraries_router, prefix="/api/v1", tags=["itineraries"])  # Correctly reference itineraries router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
