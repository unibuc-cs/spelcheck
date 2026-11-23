# Visitors Specification

## Purpose

Visitors check in at the entrance of a hospital ward.

## Requirements

### Requirement: Check-in

#### Scenario: Listed visitor

- **WHEN** a visitor checks in at a ward
- **AND** the visitor is on the patient's visitor list
- **THEN** the system opens the ward door and prints a visitor badge

#### Scenario: Unlisted visitor

- **WHEN** a visitor checks in at a ward
- **AND** the visitor is not on the patient's visitor list
- **THEN** the system keeps the ward door closed and calls a nurse

### Requirement: Hours

#### Scenario: End of visiting time

- **WHEN** visiting time ends
- **THEN** the system reminds all visitors to leave

### Requirement: Safety

#### Scenario: Badge not returned

- **WHEN** a visitor leaves without returning the badge for the second time
- **THEN** the system informs the ward manager

### Requirement: Hours

#### Scenario: Long visit

- **WHEN** a visitor has stayed for more than 2 hours
- **THEN** the system asks the visitor to make room for others

### Requirement: Safety

#### Scenario: Isolation

- **WHEN** the patient is in isolation
- **THEN** the system keeps the ward door closed for visitors
