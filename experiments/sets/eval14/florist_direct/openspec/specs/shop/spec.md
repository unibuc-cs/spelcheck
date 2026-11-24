# shop Specification

## Purpose

Loyalty cards, complaints, and the arrival of fresh flowers.

## Requirements

### Requirement: Loyalty cards

The system SHALL reward regular customers.

#### Scenario: Card full

- **WHEN** a customer shows a loyalty card
- **AND** the card is full
- **THEN** the system gives the customer a free bouquet

#### Scenario: Card not full

- **WHEN** a customer shows a loyalty card
- **AND** the card is not full
- **THEN** the system adds a stamp to the card

### Requirement: Complaints

The system SHALL act on complaints about wilted flowers.

#### Scenario: Third complaint

- **WHEN** a customer complains about wilted flowers for the third time
- **THEN** the system informs the owner

### Requirement: Fresh flowers

The system SHALL announce the arrival of fresh flowers.

#### Scenario: Truck unloading

- **WHEN** the flower truck is being unloaded
- **THEN** the system shows a notice at the counter
