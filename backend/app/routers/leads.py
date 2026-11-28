from fastapi import APIRouter
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import LeadService
import json

router = APIRouter(prefix="/api/v1/leads", tags=["Leads"])

# Yahan se 'backend/' hata diya hai
JSON_FILE = "leads.json" 

@router.post("/", response_model=LeadResponse)
def create_lead(lead: LeadCreate):
    llm_result = LeadService.classify_lead(lead)
    new_lead = {
        "id": 1,
        "name": lead.name,
        "email": lead.email,
        "message": lead.message,
        "source": lead.source,
        "category": llm_result.get("category", "Cold"),
        "reply": llm_result.get("reply", "Thank you.")
    }
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    
    new_lead["id"] = len(data) + 1
    data.append(new_lead)
    
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    return new_lead