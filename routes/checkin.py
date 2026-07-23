from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.booking import Booking
from models.checkin import CheckIn
from models.event import Event
from models.user import User

router = APIRouter(
    prefix="/checkin",
    tags=["QR Check-In"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/{booking_id}")
def qr_checkin(
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

    if booking.booking_status == "Cancelled":

        raise HTTPException(
            status_code=400,
            detail="Cancelled booking cannot be checked in."
        )

    existing = db.query(CheckIn).filter(
        CheckIn.booking_id == booking_id
    ).first()

    if existing and existing.checked_in:

        raise HTTPException(
            status_code=400,
            detail="QR Check-in already completed."
        )

    checkin = CheckIn(
        booking_id=booking_id,
        checkin_time=datetime.now(),
        checked_in=True
    )

    db.add(checkin)
    db.commit()
    db.refresh(checkin)

    return {
        "message": "Check-in successful.",
        "checkin": checkin
    }


@router.get("/events/{event_id}/attendees")
def event_attendees(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    attendees = (
        db.query(User)
        .join(Booking, User.id == Booking.attendee_id)
        .filter(Booking.event_id == event_id)
        .all()
    )

    return attendees


@router.get("/reports/tickets/{event_id}")
def ticket_report(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:

        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    sold = event.total_tickets - event.available_tickets

    return {
        "event_name": event.event_name,
        "total_tickets": event.total_tickets,
        "sold_tickets": sold,
        "available_tickets": event.available_tickets
    }


@router.get("/history/{attendee_id}")
def booking_history(
    attendee_id: int,
    db: Session = Depends(get_db)
):

    attendee = db.query(User).filter(
        User.id == attendee_id
    ).first()

    if not attendee:

        raise HTTPException(
            status_code=404,
            detail="Attendee not found."
        )

    history = db.query(Booking).filter(
        Booking.attendee_id == attendee_id
    ).all()

    return history
