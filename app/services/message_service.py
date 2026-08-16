from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.message import TicketMessage
from app.schemas.message import MessageCreate


def get_messages_for_ticket(db: Session, ticket_id: str) -> list[TicketMessage]:
    """
    Fetch all messages for a specific ticket, oldest first.
    """
    return (
        db.query(TicketMessage)
        .filter(TicketMessage.ticket_id == ticket_id)
        .order_by(TicketMessage.created_at.asc())
        .all()
    )


def create_message(db: Session, ticket_id: str, message_data: MessageCreate) -> TicketMessage | None:
    """
    Add a new message to a ticket.
    Returns None if the ticket doesn't exist.
    """
    # Verify the ticket exists before adding a message
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket is None:
        return None

    new_message = TicketMessage(
        ticket_id=ticket_id,
        message_text=message_data.message_text,
        author=message_data.author,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
