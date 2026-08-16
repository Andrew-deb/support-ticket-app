from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketStatusUpdate


def get_all_tickets(db: Session) -> list[Ticket]:
    """
    Fetch all tickets, newest first.
    """
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()


def get_ticket_by_id(db: Session, ticket_id: str) -> Ticket | None:
    """
    Fetch a single ticket by ID.
    Returns None if not found (the route decides what HTTP error to return).
    """
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()


def create_ticket(db: Session, ticket_data: TicketCreate) -> Ticket:
    """
    Create a new ticket in the database.
    """
    new_ticket = Ticket(
        title=ticket_data.title,
        status=ticket_data.status,
        created_by=ticket_data.created_by,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)  # Get the auto-generated ticket_id and created_at
    return new_ticket


def update_ticket_status(db: Session, ticket_id: str, update_data: TicketStatusUpdate) -> Ticket | None:
    """
    Update a ticket's status.
    Returns None if the ticket doesn't exist.
    """
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket is None:
        return None

    ticket.status = update_data.status  
    db.commit()                          
    db.refresh(ticket)                  
    return ticket

def delete_ticket(db: Session, ticket_id: str) -> bool:
    """
    Delete a ticket by ID.
    Returns True if deleted, False if ticket didn't exist.
    
    The ON DELETE CASCADE in the database schema means
    all messages for this ticket are automatically deleted too.
    """
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket is None:
        return False

    db.delete(ticket)
    db.commit()
    return True
