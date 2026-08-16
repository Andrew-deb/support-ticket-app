from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class MessageCreate(BaseModel):
    message_text: str
    author: str


class MessageResponse(BaseModel):
    message_id: UUID
    ticket_id: UUID
    message_text: str
    author: str
    created_at: datetime

    model_config = {"from_attributes": True}