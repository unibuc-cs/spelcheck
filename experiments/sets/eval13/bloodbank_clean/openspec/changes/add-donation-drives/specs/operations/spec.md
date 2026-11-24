## ADDED Requirements

### Requirement: Donation drives

The system SHALL plan donation drives at companies.

#### Scenario: Bus free

- **WHEN** a company asks for a donation drive
- **AND** the donation bus is free on that day
- **THEN** the system books the bus and confirms the date

#### Scenario: Bus not free

- **WHEN** a company asks for a donation drive
- **AND** the donation bus is not free on that day
- **THEN** the system offers the company another date
