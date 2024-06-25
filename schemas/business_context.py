from pydantic import BaseModel

class BusinessContext(BaseModel):
    ownerName: str
    businessName: str
    businessDescription: str
    persona: str