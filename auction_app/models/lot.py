import uuid
from sqlalchemy import UUID, String, Numeric, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from decimal import Decimal
from .base import Base
from auction_app.core.lot_status_enum import LotStatus


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(String, nullable=False)

    start_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    current_price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    status: Mapped[LotStatus] = mapped_column(
        Enum(LotStatus),
        default=LotStatus.running,
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    bids: Mapped[list["Bid"]] = relationship(
        "Bid",
        back_populates="lot"
    )


