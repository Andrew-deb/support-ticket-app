from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services import message_service

router = APIRouter(prefix="/api/tickets", tags=["messages"])


@router.get("/{ticket_id}/messages", response_model=list[MessageResponse])
def get_messages(ticket_id: str, db: Session = Depends(get_db)):
    """GET /api/tickets/{ticket_id}/messages — Fetch all messages for a ticket."""
    messages = message_service.get_messages_for_ticket(db, ticket_id)
    return messages


@router.post("/{ticket_id}/messages", response_model=MessageResponse, status_code=201)
def create_message(ticket_id: str, message: MessageCreate, db: Session = Depends(get_db)):
    """POST /api/tickets/{ticket_id}/messages — Add a message to a ticket."""
    new_message = message_service.create_message(db, ticket_id, message)
    if new_message is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return new_message
