## ADDED Requirements

### Requirement: Interview room

The system SHALL plan the use of the interview room.

#### Scenario: Room free

- **WHEN** a reporter asks for the interview room
- **AND** the room is free at that time
- **THEN** the system books the room for the reporter

#### Scenario: Room not free

- **WHEN** a reporter asks for the interview room
- **AND** the room is not free at that time
- **THEN** the system offers the reporter the next free hour
