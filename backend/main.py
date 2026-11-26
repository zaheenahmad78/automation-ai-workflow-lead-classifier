from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime

app = FastAPI()

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model
class LeadInput(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    source: str

# File storage
LEADS_FILE = "leads.json"

def load_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

# Classification function
def classify_lead(message: str):
    msg = message.lower()
    
    # Hot leads - urgent, high intent
    if any(word in msg for word in ["urgent", "immediately", "asap", "emergency", "critical", "need this", "right now"]):
        return "Hot", "Thanks for your urgent inquiry! Our team will contact you within 1 hour."
    
    # Warm leads - interested but not urgent
    elif any(word in msg for word in ["interested", "pricing", "demo", "quote", "buy", "tell me more", "information"]):
        return "Warm", "Thank you for your interest! We'll send you more information shortly."
    
    # Cold leads - just browsing, spam, or no intent
    else:
        return "Cold", "Thanks for reaching out! We'll get back to you within 48 hours."

# API Endpoints
@app.post("/lead")
async def create_lead(lead: LeadInput):
    leads = load_leads()
    classification, reply = classify_lead(lead.message)
    
    new_id = max([l.get("id", 0) for l in leads], default=0) + 1
    
    new_lead = {
        **lead.model_dump(),
        "id": new_id,
        "classification": classification,
        "suggested_reply": reply,
        "status": "new",
        "created_at": datetime.now().isoformat()
    }
    
    leads.append(new_lead)
    save_leads(leads)
    print(f"✅ New lead: {lead.name} - {classification}")
    return new_lead

@app.get("/leads")
async def get_leads(classification: Optional[str] = None):
    leads = load_leads()
    if classification:
        leads = [l for l in leads if l["classification"] == classification]
    return leads

@app.patch("/lead/{lead_id}/contact")
async def mark_contacted(lead_id: int):
    leads = load_leads()
    for lead in leads:
        if lead["id"] == lead_id:
            lead["status"] = "contacted"
            save_leads(leads)
            return {"success": True}
    raise HTTPException(status_code=404, detail="Lead not found")

@app.delete("/lead/{lead_id}")
async def delete_lead(lead_id: int):
    leads = load_leads()
    leads = [l for l in leads if l["id"] != lead_id]
    save_leads(leads)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 SERVER STARTING...")
    print("="*50)
    print("📝 API Docs: http://localhost:8000/docs")
    print("📊 GET /leads - View all leads")
    print("➕ POST /lead - Add new lead")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)