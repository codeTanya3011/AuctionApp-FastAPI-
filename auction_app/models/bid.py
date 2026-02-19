import uuid
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime
from decimal import Decimal
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc))

    lot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lots.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    lot: Mapped["Lot"] = relationship(
        "Lot",
        back_populates="bids"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="bids"
    )


