## MODIFIED Requirements

### Requirement: Room doors

The system SHALL control the room doors by card.

#### Scenario: Valid card

- **WHEN** a student holds the card to a room door
- **AND** the card is valid for that room
- **THEN** the system unlocks the room door

#### Scenario: Other card

- **WHEN** a student holds the card to a room door
- **AND** the card is not valid for that room
- **THEN** the system keeps the room door locked and records the attempt
