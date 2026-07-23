from datetime import date


VALID_EVENT_STATUS = [
    "Upcoming",
    "Ongoing",
    "Completed",
    "Cancelled"
]

VALID_BOOKING_STATUS = [
    "Booked",
    "Confirmed",
    "Cancelled"
]


def valid_event_status(status):

    return status in VALID_EVENT_STATUS


def valid_booking_status(status):

    return status in VALID_BOOKING_STATUS


def future_event(event_date):

    return event_date > date.today()


def valid_ticket_price(price):

    return price > 0


def valid_ticket_count(count):

    return count > 0


def enough_tickets(
    available,
    requested
):

    return available >= requested


def calculate_total_amount(
    ticket_price,
    ticket_count
):

    return ticket_price * ticket_count
