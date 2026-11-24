# operations Specification

## Purpose

Orders of the hospitals, the fridges, and what the staff is told.

## Requirements

### Requirement: Hospital orders

The system SHALL serve the orders of the hospitals.

#### Scenario: In stock

- **WHEN** a hospital orders blood
- **AND** the blood group is in stock
- **THEN** the system reserves the units and prints a delivery note

#### Scenario: Not in stock

- **WHEN** a hospital orders blood
- **AND** the blood group is not in stock
- **THEN** the system asks the neighbouring blood bank

### Requirement: Fridges

The system SHALL watch the fridges.

#### Scenario: Fridge too warm

- **WHEN** a fridge reports a temperature above 6 degrees
- **THEN** the system alerts the technician on duty

### Requirement: Postal strike

The system SHALL hold back the post during a strike.

#### Scenario: Strike

- **WHEN** the postal service is on strike
- **THEN** the system does not send any letter

### Requirement: Stocktaking

The system SHALL announce the stocktaking.

#### Scenario: Stocktaking running

- **WHEN** the stocktaking is running
- **THEN** the system shows a notice to the staff
