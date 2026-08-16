import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class TicketMessage(Base):
    """
    SQLAlchemy ORM model for the 'ticket_messages' table.
    """

    __tablename__ = "ticket_messages"

    message_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    ticket_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tickets.ticket_id", ondelete="CASCADE"),
        nullable=False,
    )
    message_text = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    ticket = relationship("Ticket", back_populates="messages")
