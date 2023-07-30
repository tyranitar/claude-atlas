from typing import List, Optional

from pydantic import BaseModel

class ItineraryBlock(BaseModel):
    name: str

class ItineraryRequest(BaseModel):
    city: str
    context: Optional[str]

class ItineraryResponse(BaseModel):
    response: List[ItineraryBlock]
