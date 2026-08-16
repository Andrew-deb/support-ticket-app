from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ticket import TicketCreate, TicketStatusUpdate, TicketResponse
from app.services import ticket_service

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.get("/", response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    """
    GET /api/tickets — Fetch all tickets.
    
    Notice how clean this is:
    - The route doesn't know about SQL or database connections
    - Depends(get_db) automatically provides a session and closes it after
    - response_model tells FastAPI to format the output as TicketResponse objects
    """
    tickets = ticket_service.get_all_tickets(db)
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """GET /api/tickets/{ticket_id} — Fetch one ticket."""
    ticket = ticket_service.get_ticket_by_id(db, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.post("/", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """POST /api/tickets — Create a new ticket."""
    new_ticket = ticket_service.create_ticket(db, ticket)
    return new_ticket


@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(ticket_id: str, update: TicketStatusUpdate, db: Session = Depends(get_db)):
    """PATCH /api/tickets/{ticket_id}/status — Update a ticket's status."""
    ticket = ticket_service.update_ticket_status(db, ticket_id, update)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """DELETE /api/tickets/{ticket_id} — Delete a ticket and all its messages."""
    deleted = ticket_service.delete_ticket(db, ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")

