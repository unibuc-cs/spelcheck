# programme Specification

## Purpose

The museum offers guided tours and hosts private events.

## Requirements

### Requirement: Guided tours

The system SHALL take bookings for guided tours.

#### Scenario: Tour booking

- **WHEN** a visitor books a guided tour
- **THEN** the system reserves a place on the tour and sends a confirmation

### Requirement: Private events

The system SHALL announce private events.

#### Scenario: Announcement

- **WHEN** a private event is taking place in the museum
- **THEN** the system shows a notice at the entrance

### Requirement: No-shows

The system SHALL keep track of visitors who miss their tours.

#### Scenario: Second missed tour

- **WHEN** a visitor misses a booked tour for the second time
- **THEN** the system asks the visitor to pay in advance for the next booking
