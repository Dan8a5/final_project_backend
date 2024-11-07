from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from app.models.park import Park
from app.dependencies import get_db
from typing import List, Optional

router = APIRouter(prefix="/parks", tags=["parks"])

@router.get("", response_model=List[Park])
async def get_parks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get a list of parks with pagination.
    """
    query = select(Park)
    parks = db.exec(query.offset(skip).limit(limit)).all()
    return parks

@router.get("/{park_id}", response_model=Park)
async def get_park(
    park_id: str,  # Changed to str as it's uuid
    db: Session = Depends(get_db)
):
    """
    Get a specific park by ID.
    """
    park = db.get(Park, park_id)
    if not park:
        raise HTTPException(status_code=404, detail="Park not found")
    return park

@router.get("/search/", response_model=List[Park])
async def search_parks(
    q: str = Query(None, description="Search term for park name or description"),
    db: Session = Depends(get_db)
):
    """
    Search parks by description (since we don't have a name field).
    """
    query = select(Park)
    
    if q:
        query = query.where(Park.description.ilike(f"%{q}%"))
    
    parks = db.exec(query).all()
    return parks

@router.get("/parkcode/{parkcode}", response_model=Park)
async def get_park_by_code(
    parkcode: str,
    db: Session = Depends(get_db)
):
    """
    Get a park by its parkcode.
    """
    park = db.exec(select(Park).where(Park.parkcode == parkcode)).first()
    if not park:
        raise HTTPException(status_code=404, detail=f"Park with code {parkcode} not found")
    return park