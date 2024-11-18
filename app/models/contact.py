from pydantic import BaseModel
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: str
    message: str

class Contact(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: datetime
    user_id: str
