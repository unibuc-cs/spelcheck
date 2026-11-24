# rooms Specification

## Purpose

Students move into a dormitory and open their rooms with a card.

## Requirements

### Requirement: Move-in with deposit

The system SHALL hand out a room when the deposit is paid.

#### Scenario: Deposit paid

- **WHEN** a student arrives to move in
- **AND** the deposit is paid
- **THEN** the system assigns a room and activates the student's card

### Requirement: Move-in without deposit

The system SHALL hold back the room until the deposit is paid.

#### Scenario: Deposit not paid

- **WHEN** a student arrives to move in
- **AND** the deposit is not paid
- **THEN** the system sends the student to the housing office

### Requirement: Room doors

The system SHALL control the room doors by card.

#### Scenario: Valid card

- **WHEN** a student holds the card to a room door
- **AND** the card is valid for that room
- **THEN** the system unlocks the room door

#### Scenario: Other card

- **WHEN** a student holds the card to a room door
- **AND** the card is not valid for that room
- **THEN** the system keeps the room door locked
