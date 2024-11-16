from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlmodel import Session, select, or_  # Add or_ import
from app.models.park import Park
from app.dependencies import get_db, get_current_user
from typing import List
import logging

router = APIRouter(prefix="/parks", tags=["parks"])

@router.get("", response_model=List[Park])
async def get_parks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get a list of parks with pagination.
    """
    try:
        query = select(Park).offset(skip).limit(limit)
        parks = db.exec(query).all()
        logging.info(f"Retrieved {len(parks)} parks")
        return parks
    except Exception as e:
        logging.error(f"Error retrieving parks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/parkcode/{parkcode}", response_model=Park)
async def get_park_by_parkcode(
    parkcode: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific park using its parkcode
    Example: /api/v1/parks/parkcode/yose (for Yosemite)
    """
    try:
        query = select(Park).where(Park.parkcode == parkcode.lower())
        park = db.exec(query).first()
        
        if not park:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Park with code '{parkcode}' not found"
            )
            
        logging.info(f"Retrieved park details for {parkcode}")
        return park
        
    except Exception as e:
        logging.error(f"Error retrieving park with code {parkcode}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving park: {str(e)}"
        )

@router.get("/search", response_model=List[Park])
async def search_parks(
    q: str = Query(None, description="Search parks by name or description"),
    db: Session = Depends(get_db)
):
    """
    Search parks by name or description.
    Examples: 
    - /parks/search?q=Yosemite
    - /parks/search?q=Canyon
    - /parks/search?q=wilderness
    """
    try:
        query = select(Park)
        if q:
            # Search in both name and description fields
            query = query.where(
                or_(
                    Park.name.ilike(f"%{q}%"),
                    Park.description.ilike(f"%{q}%")
                )
            )
        
        parks = db.exec(query).all()
        logging.info(f"Found {len(parks)} parks matching search term '{q}'")
        return parks
    except Exception as e:
        logging.error(f"Error searching parks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )