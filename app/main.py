from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes.parks import router as parks_router
from app.routes.itineraries import itineraries_router
from app.routes.contact import contact_router
from app.config.config import engine
from sqlmodel import SQLModel

app = FastAPI(
    title="National Parks Explorer API",
    description="API for exploring US National Parks, creating itineraries, and getting park information",
    version="1.0.0"
)

async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app.lifespan = lifespan

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://trailtrek.netlify.app/"
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
            "authentication": "/auth",
            "parks": "/parks",
            "itineraries": "/itineraries",
            "contact": "/contact",
            "version": "1.0.0"
        }
    }

# Include routers without prefix
app.include_router(auth.router)
app.include_router(parks_router)
app.include_router(itineraries_router, tags=["itineraries"])
app.include_router(contact_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
