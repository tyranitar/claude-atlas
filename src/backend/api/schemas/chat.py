from typing import List

from pydantic import BaseModel


class BaseChat(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[BaseChat]
