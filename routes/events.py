from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.event import Event
from schemas.event import EventCreate
from services.event_service import (
    future_event,
    valid_event_status
)

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db)
):

    if not future_event(event.event_date):

        raise HTTPException(
            status_code=400,
            detail="Event date must be in the future."
        )

    if not valid_event_status(event.status):

        raise HTTPException(
            status_code=400,
            detail="Invalid event status."
        )

    db_event = Event(**event.dict())

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


@router.get("/")
def get_events(
    event_name: str = None,
    venue: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Event)

    if event_name:
        query = query.filter(Event.event_name.contains(event_name))

    if venue:
        query = query.filter(Event.venue.contains(venue))

    if status:
        query = query.filter(Event.status == status)

    total = query.count()

    events = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": events
    }


@router.get("/{event_id}")
def get_event(
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

    return event


@router.put("/{event_id}")
def update_event(
    event_id: int,
    event: EventCreate,
    db: Session = Depends(get_db)
):

    db_event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not db_event:

        raise HTTPException(
            status_code=404,
            detail="Event not found."
        )

    for key, value in event.dict().items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)

    return db_event


@router.delete("/{event_id}")
def delete_event(
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

    db.delete(event)
    db.commit()

    return {
        "message": "Event deleted successfully."
    }
