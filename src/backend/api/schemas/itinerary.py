from typing import List, Optional

from pydantic import BaseModel

class ItineraryBlock(BaseModel):
    name: str
    latitude: float
    longitude: float
    start_time: str
    end_time: str

class ItineraryRequest(BaseModel):
    city: str
    quest: str
    context: Optional[str]

class ItineraryResponse(BaseModel):
    response: List[ItineraryBlock]
