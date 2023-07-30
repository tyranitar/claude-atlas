from typing import List, Optional

from pydantic import BaseModel

class ItineraryBlock(BaseModel):
    name: str
    latitude: float
    longitude: float
    start_time: str
    end_time: str
    image_url: str

class ItineraryRequest(BaseModel):
    city: str
    quest: str

class ItineraryResponse(BaseModel):
    response: List[ItineraryBlock]
