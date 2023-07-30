from typing import List

from pydantic import BaseModel

from api.schemas.itinerary import ItineraryBlock

class SyncCalendarRequest(BaseModel):
    events: List[ItineraryBlock]

class SyncCalendarResponse(BaseModel):
    status_code: int
