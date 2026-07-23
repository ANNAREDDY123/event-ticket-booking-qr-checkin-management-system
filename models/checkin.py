from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from database import Base


class CheckIn(Base):

    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        unique=True,
        nullable=False
    )

    checkin_time = Column(DateTime, nullable=True)

    checked_in = Column(
        Boolean,
        default=False
    )
