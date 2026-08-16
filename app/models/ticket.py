import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Ticket(Base):
    """
    SQLAlchemy ORM model for the 'tickets' table.
    
    """

    __tablename__ = "tickets"

    ticket_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="open")
    created_by = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('open', 'in_progress', 'resolved')",
            name="check_ticket_status"
        ),
    )

    messages = relationship(
        "TicketMessage",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )
