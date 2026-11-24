# passports Specification

## Purpose

Citizens renew their passports online.

## Requirements

### Requirement: Renewal

The system SHALL handle renewal.

#### Scenario: Valid old passport

- **WHEN** a citizen applies for a new passport
- **AND** the old passport is still valid
- **THEN** the system accepts the application online

#### Scenario: Expired old passport

- **WHEN** a citizen applies for a new passport
- **AND** the old passport has expired
- **THEN** the system books an appointment at the passport office

### Requirement: Payment

The system SHALL handle payment.

#### Scenario: Fee

- **WHEN** a citizen pays the passport fee
- **THEN** the system starts the production of the passport

### Requirement: Delivery

The system SHALL handle delivery.

#### Scenario: Ready

- **WHEN** a new passport is ready
- **THEN** the system sends the citizen a text message

### Requirement: Security

The system SHALL handle security.

#### Scenario: Lost passports

- **WHEN** a citizen reports a passport lost for the second time in five years
- **THEN** the system asks the citizen to come to the office in person
