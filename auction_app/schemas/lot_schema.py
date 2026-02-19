from decimal import Decimal
from uuid import UUID
from ..core import LotStatus
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LotBase(BaseModel):
    title: str
    start_price: Decimal
    end_time: datetime


class LotCreate(LotBase):
    pass


class LotOut(LotBase):
    id: UUID
    current_price: Decimal
    status: LotStatus

    model_config = ConfigDict(from_attributes=True)