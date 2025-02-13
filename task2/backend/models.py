from pydantic import BaseModel
from typing import Optional

class Dialogue(BaseModel):
    movie: str
    character: str
    dialogue: str

class ChatRequest(BaseModel):
    user_message: str
    character: Optional[str] = None  # User can specify a character (optional)
