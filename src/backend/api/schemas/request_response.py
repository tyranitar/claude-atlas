from typing import List, Optional

from pydantic import BaseModel


# Shared structures
class ItineraryRequest(BaseModel):
    location: Optional[str] = None
    context: Optional[str] = None

# Chat structures
class BaseChat(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[BaseChat]
