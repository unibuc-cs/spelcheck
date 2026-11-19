# Parking Specification

## Purpose

The parking garage lets cars in and out and makes sure every stay is paid.

## Requirements

### Requirement: Entry

#### Scenario: Space available

- **WHEN** a car arrives at the entry
- **AND** a space is free
- **THEN** the system opens the entry barrier

#### Scenario: Garage full

- **WHEN** a car arrives at the entry
- **AND** no space is free
- **THEN** the system keeps the entry barrier closed and shows FULL

### Requirement: Exit

#### Scenario: Paid ticket

- **WHEN** a car arrives at the exit
- **AND** its ticket is paid
- **THEN** the system opens the exit barrier

#### Scenario: Unpaid ticket

- **WHEN** a car arrives at the exit
- **AND** its ticket is not paid
- **THEN** the system keeps the exit barrier closed

### Requirement: Payment

#### Scenario: Paying

- **WHEN** a driver pays a ticket
- **THEN** the system marks the ticket as paid
