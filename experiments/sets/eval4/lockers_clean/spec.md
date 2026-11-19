# Lockers Specification

## Purpose

Couriers leave parcels in lockers; recipients open their compartment with a pickup code.

## Requirements

### Requirement: Delivery

#### Scenario: Free compartment

- **WHEN** a courier scans a parcel
- **AND** a compartment of the right size is free
- **THEN** the system opens that compartment and sends a pickup code to the recipient

#### Scenario: Locker full

- **WHEN** a courier scans a parcel
- **AND** no compartment of the right size is free
- **THEN** the system shows the courier the nearest locker with space

### Requirement: Pickup

#### Scenario: Correct code

- **WHEN** a recipient enters a correct pickup code
- **THEN** the system opens the compartment of the parcel

#### Scenario: Wrong code

- **WHEN** a recipient enters a wrong pickup code for the third time
- **THEN** the system locks the keypad for ten minutes and alerts the recipient

### Requirement: Expiry

#### Scenario: Not collected

- **WHEN** a parcel has been in its compartment for more than 72 hours
- **THEN** the system sends a last reminder to the recipient
