# operations Specification

## Purpose

What the staff of the cinema is told and asked to do.

## Requirements

### Requirement: Snack orders

The system SHALL take snack orders from the seats.

#### Scenario: Order from a seat

- **WHEN** a customer orders snacks from a seat
- **THEN** the system sends the order to the kiosk and charges the customer's card

### Requirement: Projector

The system SHALL report projector trouble.

#### Scenario: Projector fault

- **WHEN** the projector of a hall is out of order
- **THEN** the system informs the technician on duty

### Requirement: Cleaning

The system SHALL react to complaints about dirty halls.

#### Scenario: Third complaint

- **WHEN** customers complain about a dirty hall for the third time in a week
- **THEN** the system orders an extra cleaning
