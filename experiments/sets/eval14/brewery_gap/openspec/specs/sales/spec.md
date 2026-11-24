# sales Specification

## Purpose

Orders of the shops, complaints, and what the brewers are told.

## Requirements

### Requirement: Shop orders

The system SHALL serve the orders of the shops.

#### Scenario: Beer in stock

- **WHEN** a shop orders beer
- **AND** the beer is in stock
- **THEN** the system prints a delivery note

#### Scenario: Beer not in stock

- **WHEN** a shop orders beer
- **AND** the beer is not in stock
- **THEN** the system tells the shop the next bottling date

### Requirement: Complaints

The system SHALL act on complaints about a batch.

#### Scenario: Third complaint

- **WHEN** a shop complains about a batch for the third time
- **THEN** the system recalls the batch

### Requirement: Cleaning

The system SHALL announce the cleaning of the brewhouse.

#### Scenario: Cleaning day

- **WHEN** the brewhouse is being cleaned
- **THEN** the system shows a notice to the brewers
