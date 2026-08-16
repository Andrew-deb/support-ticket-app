from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TicketCreate(BaseModel):
    title: str
    created_by: str
    status: str = "open"


class TicketStatusUpdate(BaseModel):
    status: str


class TicketResponse(BaseModel):
    ticket_id: UUID
    title: str
    status: str
    created_by: str
    created_at: datetime

    model_config = {"from_attributes": True}