from pydantic import BaseModel, EmailStr
from enum import Enum

class LeadCategory(str, Enum):
    HOT = "Hot"
    WARM = "Warm"
    COLD = "Cold"

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    message: str
    source: str

class LeadResponse(LeadCreate):
    id: int
    category: LeadCategory
    reply: str

    class Config:
        from_attributes = True