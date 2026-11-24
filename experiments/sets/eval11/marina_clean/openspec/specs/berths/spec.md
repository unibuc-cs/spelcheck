# berths Specification

## Purpose

Visiting boats get a guest berth and pay for their stay.

## Requirements

### Requirement: Guest berths

The system SHALL give guest berths to visiting boats.

#### Scenario: Berth free

- **WHEN** a skipper asks for a guest berth
- **AND** a guest berth is free
- **THEN** the system assigns the berth and shows its number

#### Scenario: No berth free

- **WHEN** a skipper asks for a guest berth
- **AND** no guest berth is free
- **THEN** the system sends the skipper to the anchorage

### Requirement: Departure

The system SHALL close the stay when a boat leaves.

#### Scenario: Boat leaves

- **WHEN** a skipper reports the departure of the boat
- **THEN** the system frees the berth and sends the invoice for the stay
