from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.booking import Booking
from models.event import Event
from models.user import User
from schemas.booking import BookingCreate
from services.event_service import (
    enough_tickets,
    valid_booking_status,
    calculate_total_amount
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    attendee = db.query(User).filter(
        User.id == booking.attendee_id
    ).first()

    if not attendee:

        raise HTTPException(
            status_code=404,
            detail="Attendee not found."
        )

    event = db.query(Event).filter(
        Event.id == booking.event_id
    ).first()

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    if not enough_tickets(
        event.available_tickets,
        booking.ticket_count
    ):

        raise HTTPException(
            status_code=400,
            detail="Not enough tickets available."
        )

    if not valid_booking_status(
        booking.booking_status
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid booking status."
        )

    total = calculate_total_amount(
        event.ticket_price,
        booking.ticket_count
    )

    db_booking = Booking(
        attendee_id=booking.attendee_id,
        event_id=booking.event_id,
        ticket_count=booking.ticket_count,
        total_amount=total,
        booking_status=booking.booking_status
    )

    event.available_tickets -= booking.ticket_count

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking


@router.get("/")
def get_bookings(
    attendee_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Booking)

    if attendee_id:
        query = query.filter(
            Booking.attendee_id == attendee_id
        )

    total = query.count()

    bookings = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": bookings
    }


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    return booking


@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    db_booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not db_booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    event = db.query(Event).filter(
        Event.id == booking.event_id
    ).first()

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    if booking.booking_status == "Cancelled":
        event.available_tickets += db_booking.ticket_count

    db_booking.attendee_id = booking.attendee_id
    db_booking.event_id = booking.event_id
    db_booking.ticket_count = booking.ticket_count
    db_booking.total_amount = calculate_total_amount(
        event.ticket_price,
        booking.ticket_count
    )
    db_booking.booking_status = booking.booking_status

    db.commit()
    db.refresh(db_booking)

    return db_booking
