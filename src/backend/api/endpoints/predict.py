from fastapi import APIRouter

from api.schemas.request_response import ItineraryRequest, ChatRequest
from api.core.agent import AgentEngine

router = APIRouter()
agent = AgentEngine()

@router.post("/predict/")
async def predict(request: ItineraryRequest):
    resp = agent.generate_responses(request)
    return await resp


@router.post("/chat/")
async def chat(request: ChatRequest):
    result = agent.compute_chat_response(request=request)

    return {"status": "success", "message": result}
