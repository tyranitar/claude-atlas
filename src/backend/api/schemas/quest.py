from typing import List, Optional

from pydantic import BaseModel

class Quest(BaseModel):
    name: str
    image_url: str
    fun_facts: List[str]

class QuestRequest(BaseModel):
    city: Optional[str] = None
    rejected_options: Optional[List[str]] = None

class QuestResponse(BaseModel):
    response: List[Quest]
