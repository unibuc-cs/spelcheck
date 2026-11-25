# dome Specification

## Purpose

Telescope time, cancellations, and notices.

## Requirements

### Requirement: Telescope time

The system SHALL give telescope time to visitors.

#### Scenario: Telescope free

- **WHEN** a visitor asks for telescope time
- **AND** the telescope is free
- **THEN** the system unlocks the telescope controls

#### Scenario: Telescope in use

- **WHEN** a visitor asks for telescope time
- **AND** the telescope is not free
- **THEN** the system puts the visitor on the telescope list

### Requirement: Late cancellations

The system SHALL act on visitors who cancel late.

#### Scenario: Second late cancellation

- **WHEN** a visitor cancels an evening on the same day for the second time
- **THEN** the system asks the visitor for a deposit

### Requirement: Mirror cleaning

The system SHALL announce the cleaning of the mirror.

#### Scenario: Mirror being cleaned

- **WHEN** the telescope mirror is being cleaned
- **THEN** the system shows a notice at the entrance
