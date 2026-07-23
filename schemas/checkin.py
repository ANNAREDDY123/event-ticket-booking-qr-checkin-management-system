from datetime import datetime

from pydantic import BaseModel


class CheckInResponse(BaseModel):

    id: int

    booking_id: int

    checkin_time: datetime | None

    checked_in: bool

    class Config:
        from_attributes = True
