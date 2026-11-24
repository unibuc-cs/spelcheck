# counter Specification

## Purpose

Households collect a food parcel at the counter once a week.

## Requirements

### Requirement: Collection

The system SHALL hand out food parcels at the counter.

#### Scenario: Card scanned

- **WHEN** a client scans the household card at the counter
- **THEN** the system releases a food parcel for the household

### Requirement: Stock count

The system SHALL announce the yearly stock count.

#### Scenario: Count in progress

- **WHEN** the yearly stock count is in progress
- **THEN** the system shows a notice at the counter

### Requirement: Missed collections

The system SHALL notice households that stop coming.

#### Scenario: Third missed collection

- **WHEN** a household misses its collection for the third time in a row
- **THEN** the system informs the social worker
