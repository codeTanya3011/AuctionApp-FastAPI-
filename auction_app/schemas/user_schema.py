from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)