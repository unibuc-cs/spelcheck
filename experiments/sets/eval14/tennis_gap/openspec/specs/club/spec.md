# club Specification

## Purpose

Guests, members who do not turn up, and tournaments.

## Requirements

### Requirement: Guests

The system SHALL handle the guests of members.

#### Scenario: Guest fee paid

- **WHEN** a member brings a guest
- **AND** the guest fee is paid
- **THEN** the system prints a guest ticket

#### Scenario: Guest fee not paid

- **WHEN** a member brings a guest
- **AND** the guest fee is not paid
- **THEN** the system asks for the guest fee

### Requirement: No-shows

The system SHALL act on members who do not turn up.

#### Scenario: Third no-show

- **WHEN** a member misses a booked court for the third time in a season
- **THEN** the system blocks the bookings of the member for a week

### Requirement: Tournaments

The system SHALL announce tournaments.

#### Scenario: Tournament day

- **WHEN** a tournament is being played
- **THEN** the system shows the schedule at the entrance
