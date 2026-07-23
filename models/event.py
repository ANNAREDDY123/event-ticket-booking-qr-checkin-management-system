from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String(150), nullable=False)

    venue = Column(String(200), nullable=False)

    event_date = Column(Date, nullable=False)

    total_tickets = Column(Integer, nullable=False)

    available_tickets = Column(Integer, nullable=False)

    ticket_price = Column(Float, nullable=False)

    status = Column(String(30), nullable=False)
