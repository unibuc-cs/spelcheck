# Carwash Specification

## Purpose

Customers pay at a terminal and drive their car through an automatic car wash.

## Requirements

### Requirement: Payment

#### Scenario: Paid

- **WHEN** a customer pays at the terminal
- **AND** the wash is free
- **THEN** the system opens the entry gate

#### Scenario: Busy

- **WHEN** a customer pays at the terminal
- **AND** another car is being washed
- **THEN** the system shows the waiting time

### Requirement: Washing

#### Scenario: Start

- **WHEN** a car is in position
- **AND** the entry gate is closed
- **THEN** the system starts the selected program

### Requirement: Safety

#### Scenario: Emergency stop

- **WHEN** someone presses the emergency button
- **THEN** the system stops all brushes and opens the exit gate

#### Scenario: Sensor fault

- **WHEN** the position sensor fails for the third time in a day
- **THEN** the system closes the wash and calls a technician
