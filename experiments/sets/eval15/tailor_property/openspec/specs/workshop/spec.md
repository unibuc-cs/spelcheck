# workshop Specification

## Purpose

Collection, missed fittings, and notices.

## Requirements

### Requirement: Collection

The system SHALL hand out finished garments.

#### Scenario: Alteration paid

- **WHEN** a customer collects a garment
- **AND** the alteration is paid
- **THEN** the system prints a release note

#### Scenario: Alteration not paid

- **WHEN** a customer collects a garment
- **AND** the alteration is not paid
- **THEN** the system shows the amount due

### Requirement: Missed fittings

The system SHALL act on customers who miss fittings.

#### Scenario: Second missed fitting

- **WHEN** a customer misses a fitting for the second time
- **THEN** the system asks the customer for a deposit

### Requirement: Holidays

The system SHALL announce the holidays of the shop.

#### Scenario: Shop on holiday

- **WHEN** the shop is on holiday
- **THEN** the system shows the opening date on the door
