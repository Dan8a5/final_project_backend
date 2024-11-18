from fastapi import APIRouter, Depends, Header, HTTPException

from app.models.contact import ContactCreate
from app.config.config import supabase_client
from app.dependencies import get_current_user
from datetime import datetime

contact_router = APIRouter(prefix="/contact", tags=["contact"])

@contact_router.post("")
async def create_contact(
    contact: ContactCreate,
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    try:
        if authorization and authorization.startswith('Bearer '):
            token = authorization.split(' ')[1]
            supabase_client.postgrest.auth(token)

        new_contact = {
            "user_id": current_user,
            "name": contact.name,
            "email": contact.email,
            "message": contact.message,
            "created_at": datetime.utcnow().isoformat()
        }

        response = supabase_client.table("contacts").insert(new_contact).execute()
        
        return {"message": "Contact message sent successfully", "contact": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
