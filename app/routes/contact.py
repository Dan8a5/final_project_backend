from fastapi import APIRouter, HTTPException
from app.models.contact import ContactCreate
from app.config.config import supabase_client
from datetime import datetime
from fastapi.responses import JSONResponse

contact_router = APIRouter(prefix="/contact", tags=["contact"])

@contact_router.post("", response_class=JSONResponse)
async def create_contact(contact: ContactCreate):
   """
   Create a new contact message without requiring authentication.
   """
   try:
       new_contact = {
           "name": contact.name,
           "email": contact.email,
           "message": contact.message,
           "created_at": datetime.utcnow().isoformat()
       }
       
       # Insert into Supabase
       response = supabase_client.table("contacts").insert(new_contact).execute()
       
       if not response.data:
           raise HTTPException(status_code=400, detail="Failed to create contact message")
           
       return JSONResponse(
           status_code=200,
           content={
               "message": "Contact message sent successfully",
               "contact": response.data[0]
           }
       )
       
   except Exception as e:
       raise HTTPException(
           status_code=400,
           detail=f"Error creating contact message: {str(e)}"
       )