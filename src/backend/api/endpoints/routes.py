from fastapi import APIRouter

from api.schemas.quest import QuestRequest, QuestResponse
from api.schemas.chat import ChatRequest
from api.core.agent import AgentEngine
from api.core.formatter import Formatter

router = APIRouter()
agent = AgentEngine()
formatter = Formatter()

@router.post("/quests/")
async def quests(request: QuestRequest) -> QuestResponse:
    raw_resp = agent.generate_quests(request=request)
    resp = formatter.format_itinerary(response=raw_resp)
    return resp


@router.post("/chat/")
async def chat(request: ChatRequest):
    result = agent.compute_chat_response(request=request)

    return {"status": "success", "message": result}
