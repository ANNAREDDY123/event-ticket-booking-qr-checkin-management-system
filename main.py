from fastapi import FastAPI

from database import Base, engine

from routes.auth import router as auth_router
from routes.events import router as event_router
from routes.bookings import router as booking_router
from routes.checkin import router as checkin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Ticket Booking & QR Check-in Management System"
)

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(booking_router)
app.include_router(checkin_router)


@app.get("/")
def home():
    return {
        "message": "Event Ticket Booking & QR Check-in Management System API"
    }
