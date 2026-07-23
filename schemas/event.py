from datetime import date

from pydantic import BaseModel
from pydantic import Field


class EventCreate(BaseModel):

    event_name: str = Field(..., min_length=3, max_length=150)

    venue: str = Field(..., min_length=3, max_length=200)

    event_date: date

    total_tickets: int = Field(..., gt=0)

    available_tickets: int = Field(..., ge=0)

    ticket_price: float = Field(..., gt=0)

    status: str


class EventResponse(EventCreate):

    id: int

    class Config:
        from_attributes = True
