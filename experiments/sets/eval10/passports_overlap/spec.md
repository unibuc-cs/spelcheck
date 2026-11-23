# Passports Specification

## Purpose

Citizens renew their passports online.

## Requirements

### Requirement: Renewal

#### Scenario: Valid old passport

- **WHEN** a citizen applies for a new passport
- **AND** the old passport is still valid
- **THEN** the system accepts the application online

#### Scenario: Expired old passport

- **WHEN** a citizen applies for a new passport
- **AND** the old passport has expired
- **THEN** the system books an appointment at the passport office

### Requirement: Payment

#### Scenario: Fee

- **WHEN** a citizen pays the passport fee
- **THEN** the system starts the production of the passport

### Requirement: Delivery

#### Scenario: Ready

- **WHEN** a new passport is ready
- **THEN** the system sends the citizen a text message

### Requirement: Security

#### Scenario: Lost passports

- **WHEN** a citizen reports a passport lost for the second time in five years
- **THEN** the system asks the citizen to come to the office in person

#### Scenario: Travel ban

- **WHEN** a court has banned the citizen from travelling
- **THEN** the system blocks the production of any passport for the citizen
