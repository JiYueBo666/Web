from pydantic import BaseModel


class Message(BaseModel):
    role: str = "user"
    content: str
    stream: bool = False
    is_json: bool = False
