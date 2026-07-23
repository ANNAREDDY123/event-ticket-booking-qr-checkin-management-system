from pydantic import BaseModel
from pydantic import Field


class BookingCreate(BaseModel):

    attendee_id: int

    event_id: int

    ticket_count: int = Field(..., gt=0)

    total_amount: float = Field(..., gt=0)

    booking_status: str


class BookingResponse(BookingCreate):

    id: int

    class Config:
        from_attributes = True
