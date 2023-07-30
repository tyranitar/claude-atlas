from typing import List

from pydantic import BaseModel

from api.schemas.itinerary import ItineraryBlock

class ChatRequest(BaseModel):
    city: str
    itinerary: List[ItineraryBlock]
    input: str

class ChatResponse(BaseModel):
    response: List[ItineraryBlock]
