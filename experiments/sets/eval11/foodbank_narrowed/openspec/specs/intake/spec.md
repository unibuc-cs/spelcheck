# intake Specification

## Purpose

Donors bring food, and volunteers check it and put it into the stock.

## Requirements

### Requirement: Deliveries

The system SHALL record the food that donors deliver.

#### Scenario: Within date

- **WHEN** a donor delivers food
- **AND** the food is within its use-by date
- **THEN** the system adds the food to the stock and prints a receipt

#### Scenario: Past date

- **WHEN** a donor delivers food
- **AND** the food is not within its use-by date
- **THEN** the system refuses the food and records the reason

### Requirement: Cold room

The system SHALL find a place for chilled goods.

#### Scenario: Chilled goods

- **WHEN** a volunteer scans chilled goods at the door
- **THEN** the system assigns a shelf in the cold room
