# courts Specification

## Purpose

Members of a tennis club book courts and play on them.

## Requirements

### Requirement: Booking a free court

The system SHALL give a free court to the member who asks for it.

#### Scenario: Court free

- **WHEN** a member books a court
- **AND** the court is free at that hour
- **THEN** the system reserves the court for the member

### Requirement: Booking a taken court

The system SHALL offer another hour when a court is taken.

#### Scenario: Court taken

- **WHEN** a member books a court
- **AND** the court is not free at that hour
- **THEN** the system shows the member the next free hour

### Requirement: Floodlights

The system SHALL light the courts for evening play.

#### Scenario: Evening match

- **WHEN** a member starts a match after sunset
- **THEN** the system switches the floodlights on
