CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name VARCHAR(150) NOT NULL,
    venue VARCHAR(200) NOT NULL,
    event_date DATE NOT NULL,
    total_tickets INTEGER NOT NULL,
    available_tickets INTEGER NOT NULL,
    ticket_price FLOAT NOT NULL,
    status VARCHAR(30) NOT NULL
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attendee_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    ticket_count INTEGER NOT NULL,
    total_amount FLOAT NOT NULL,
    booking_status VARCHAR(30) NOT NULL,
    FOREIGN KEY(attendee_id) REFERENCES users(id),
    FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER UNIQUE NOT NULL,
    checkin_time DATETIME,
    checked_in BOOLEAN DEFAULT FALSE,
    FOREIGN KEY(booking_id) REFERENCES bookings(id)
);
