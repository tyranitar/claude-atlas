from fastapi import APIRouter

from api.schemas.quest import QuestRequest, QuestResponse
from api.schemas.chat import ChatRequest
from api.schemas.itinerary import ItineraryRequest, ItineraryResponse
from api.schemas.gmail import SyncCalendarRequest, SyncCalendarResponse
from api.core.agent import AgentEngine
from api.core.formatter import Formatter

router = APIRouter()
formatter = Formatter()
agent = AgentEngine(formatter=formatter)

@router.post("/quests/")
def quests(request: QuestRequest) -> QuestResponse:
    raw_resp = agent.generate_quests(request=request)
    resp = formatter.format_quest(city=request.city, response=raw_resp)
    return resp


@router.post("/itinerary/")
def quests(request: ItineraryRequest) -> ItineraryResponse:
    raw_resp = agent.generate_itinerary(request=request)
    resp = formatter.format_itinerary(response=raw_resp)
    return resp


@router.post("/chat/")
def chat(request: ChatRequest) -> ItineraryResponse:
    raw_resp = agent.regenerate_itinerary(request=request)
    resp = formatter.format_regenerate_itinerary(response=raw_resp, city=request.city)
    print("raw resp...")
    print(raw_resp)

    return resp


@router.post("/sync_calendar")
def sync(request: SyncCalendarRequest) -> SyncCalendarResponse:
    resp = agent.sync_calendar(request=request)
    if resp:
        return SyncCalendarResponse(status_code=200)
    return SyncCalendarResponse(status_code=500)
