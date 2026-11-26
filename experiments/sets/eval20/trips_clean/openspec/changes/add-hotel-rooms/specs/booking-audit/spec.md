## ADDED Requirements

### Requirement: Hotel rooms

The assistant SHALL book hotel rooms.

#### Scenario: Example: a room is booked

- **WHEN** omar asks for a room in Lyon for two nights
- **AND** the hotel has a free room
- **THEN** `book_room` is called once
- **AND** the answer gives the address of the hotel

#### Scenario: Example: the hotel is full

- **WHEN** the same request runs while the hotel has no free room
- **THEN** `book_room` is never called
- **AND** the answer names another hotel

#### Scenario: Example: the traveller changes the dates

- **WHEN** the same request runs and omar changes the dates afterwards
- **THEN** `book_room` is called once
- **AND** `change_room_dates` is called once after it

### Requirement: Room audit

Every room booking SHALL be audited.

#### Scenario: Every room booking is audited

- **WHEN** a call of `book_room` succeeds
- **THEN** the run writes one audit entry that names the hotel
