from pydantic import BaseModel
from typing import List



class EmailContent(BaseModel):
    email_addresses: List[str]
    subject: str
    body: str