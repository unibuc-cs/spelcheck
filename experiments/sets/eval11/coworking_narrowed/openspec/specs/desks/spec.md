# desks Specification

## Purpose

Members book desks by the day and enter the building with a badge.

## Requirements

### Requirement: Desk booking

The system SHALL let members book a desk for a day.

#### Scenario: Desk free

- **WHEN** a member books a desk for a day
- **AND** a desk is free on that day
- **THEN** the system confirms the booking and assigns a desk

#### Scenario: No desk free

- **WHEN** a member books a desk for a day
- **AND** no desk is free on that day
- **THEN** the system puts the member on the waiting list for that day

### Requirement: Entrance

The system SHALL let members into the building.

#### Scenario: Badge at the entrance

- **WHEN** a member holds a badge to the reader at the entrance
- **THEN** the system unlocks the entrance door
