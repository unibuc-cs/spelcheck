# visits Specification

## Purpose

Visitors book and attend evenings at a public observatory.

## Requirements

### Requirement: Booking an evening with places

The system SHALL give a place to the visitor who books an evening.

#### Scenario: Places left

- **WHEN** a visitor books an evening
- **AND** the evening has places left
- **THEN** the system reserves a place for the visitor

### Requirement: Booking a full evening

The system SHALL offer another evening when one is full.

#### Scenario: Evening full

- **WHEN** a visitor books an evening
- **AND** the evening has no places left
- **THEN** the system offers the visitor the next evening

### Requirement: Dome roof

The system SHALL prepare the dome for observing.

#### Scenario: Observing starts

- **WHEN** a guide starts an observing session
- **THEN** the system opens the dome roof
