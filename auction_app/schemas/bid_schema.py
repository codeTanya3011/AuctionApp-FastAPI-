from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BidCreate(BaseModel):
    amount: Decimal
    user_id: int


class BidOut(BaseModel):
    id: int
    amount: Decimal
    created_at: datetime
    lot_id: UUID
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class BidWebSocketMessage(BaseModel):
    type: str = "bid_placed"
    lot_id: UUID
    bidder: str
    amount: Decimal