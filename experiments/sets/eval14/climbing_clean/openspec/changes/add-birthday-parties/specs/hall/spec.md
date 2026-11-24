## ADDED Requirements

### Requirement: Birthday parties

The system SHALL take bookings for birthday parties.

#### Scenario: Room free

- **WHEN** a parent books a birthday party
- **AND** the party room is free on that day
- **THEN** the system reserves the room and sends the price

#### Scenario: Room not free

- **WHEN** a parent books a birthday party
- **AND** the party room is not free on that day
- **THEN** the system offers the parent another day
