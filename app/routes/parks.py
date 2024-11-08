from fastapi import APIRouter, HTTPException, Query
from app.models.park import Park
from app.config.config import supabase_client  # Ensure you're importing your Supabase client
from typing import List

router = APIRouter(prefix="/parks", tags=["parks"])

@router.get("", response_model=List[Park])
async def get_parks(
    skip: int = 0,
    limit: int = 10
):
    """
    Get a list of parks with pagination.
    """
    # Simplified query without range for initial testing
    response = supabase_client.table("parks").select("*").execute()

    # Debugging: Print the entire response for inspection
    print("Supabase Response (get_parks):", response)

    if response.data is None:
        raise HTTPException(status_code=400, detail="Failed to fetch parks: No data found")
    elif not response.data:
        raise HTTPException(status_code=404, detail="No parks found")

    return response.data  # Return the data if no error

@router.get("/{park_id}", response_model=Park)
async def get_park(
    park_id: str,
):
    """
    Get a specific park by ID.
    """
    response = supabase_client.table("parks").select("*").eq("id", park_id).execute()

    # Debugging: Print the response for inspection
    print("Supabase Response (get_park):", response)

    if response.error or not response.data:
        raise HTTPException(status_code=404, detail="Park not found")
    
    return response.data[0]  # Return the first park found

@router.get("/search/", response_model=List[Park])
async def search_parks(
    q: str = Query(None, description="Search term for park name or description")
):
    """
    Search parks by description.
    """
    query = supabase_client.table("parks").select("*")

    if q:
        query = query.ilike("description", f"%{q}%")  # Perform a case-insensitive search
    
    response = query.execute()

    # Debugging: Print the response for inspection
    print("Supabase Response (search_parks):", response)

    if response.error:
        raise HTTPException(status_code=400, detail="Failed to search parks")
    
    return response.data  # Return the list of parks found

@router.get("/parkcode/{parkcode}", response_model=Park)
async def get_park_by_code(
    parkcode: str
):
    """
    Get a park by its parkcode.
    """
    response = supabase_client.table("parks").select("*").eq("parkcode", parkcode).execute()

    # Debugging: Print the response for inspection
    print("Supabase Response (get_park_by_code):", response)

    if response.error or not response.data:
        raise HTTPException(status_code=404, detail=f"Park with code {parkcode} not found")
    
    return response.data[0]  # Return the first park found
