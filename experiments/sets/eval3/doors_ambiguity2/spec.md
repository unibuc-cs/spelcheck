# Doors Specification

## Purpose

Office doors open with an employee badge and stay locked outside working hours.

## Requirements

### Requirement: Badge

#### Scenario: Valid badge

- **WHEN** a badge is presented
- **AND** it is within working hours
- **THEN** the system unlocks the door only for a valid badge

#### Scenario: Invalid badge

- **WHEN** a badge is presented
- **AND** the badge is not valid
- **THEN** the system keeps the door locked and logs the attempt

### Requirement: After hours

#### Scenario: Outside working hours

- **WHEN** a badge is presented
- **AND** it is outside working hours
- **AND** the badge holder is not a security guard
- **THEN** the system keeps the door locked

### Requirement: Doors

#### Scenario: Door left open

- **WHEN** a door has been open for more than 60 seconds
- **THEN** the system sounds an alarm

### Requirement: Reception

#### Scenario: Remote unlock

- **WHEN** the receptionist presses the remote button
- **THEN** the system unlocks the front door
