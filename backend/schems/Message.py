from pydantic import BaseModel
from typing import List, Optional


class HistoryMessage(BaseModel):
    role: str
    content: str


class Message(BaseModel):
    role: str = "user"
    content: str
    stream: bool = False
    is_json: bool = False
    history: Optional[List[HistoryMessage]] = []
    scene: str = "math"
