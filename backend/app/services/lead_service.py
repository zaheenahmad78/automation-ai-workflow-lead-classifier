import json
from openai import OpenAI
from app.core.config import settings
from app.schemas.lead import LeadCreate

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.GROQ_API_KEY
)

class LeadService:
    @staticmethod
    def classify_lead(lead: LeadCreate) -> dict:
        prompt = f"""
        Analyze this lead and classify it as exactly 'Hot', 'Warm', or 'Cold'.
        Also generate a personalized reply.
        Lead Name: {lead.name}
        Message: {lead.message}
        Source: {lead.source}
        
        Return ONLY a valid JSON object with exactly two keys: "category" and "reply".
        Do not include any markdown, backticks, or extra text.
        """
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # <-- Yeh Groq ka current production model hai
            messages=[{"role": "user", "content": prompt}]
            # response_format hata diya kyunki GPT-OSS isse support nahi karta
        )
        
        content = response.choices[0].message.content
        # Safety: agar model galti se markdown bhej de toh saaf karein
        content = content.replace("```json", "").replace("```", "").strip()
        
        return json.loads(content)