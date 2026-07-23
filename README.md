# event-ticket-booking-qr-checkin-management-system
A FastAPI-based Event Ticket Booking &amp; QR Check-in Management System with JWT Authentication, Role-Based Authorization, Event Management, Ticket Booking, QR Check-in, Reports, Search, Pagination, SQLAlchemy ORM, Docker Support, Logging, and Unit Testing.
# Event Ticket Booking & QR Check-in Management System

## Features

- JWT Authentication
- Role-Based Authorization
- Event Management
- Ticket Booking
- QR Check-in
- Booking History
- Sold vs Available Ticket Report
- Search & Filter
- Pagination

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Pydantic

## Installation


pip install -r requirements.txt


Run


uvicorn main:app --reload


Swagger


http://127.0.0.1:8000/docs


## Roles

- Admin
- Organizer
- Attendee

## Business Rules

- Future event dates only
- Ticket price > 0
- Ticket booking cannot exceed availability
- QR Check-in allowed only once
- Cancelled booking restores ticket availability
