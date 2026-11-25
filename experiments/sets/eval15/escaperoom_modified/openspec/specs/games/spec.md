# games Specification

## Purpose

Teams book escape rooms and play in them.

## Requirements

### Requirement: Booking a free room

The system SHALL take the booking of a free room.

#### Scenario: Room free

- **WHEN** a team books a room
- **AND** the room is free at that hour
- **THEN** the system sends the team a booking code

### Requirement: Booking a taken room

The system SHALL show other hours when a room is taken.

#### Scenario: Room taken

- **WHEN** a team books a room
- **AND** the room is not free at that hour
- **THEN** the system shows the team the free hours

### Requirement: Game start

The system SHALL start the game when the team is inside.

#### Scenario: Team enters

- **WHEN** a team enters a room
- **THEN** the system locks the room door
