# Rental Specification

## Purpose

Customers book rental cars online and return them at a branch.

## Requirements

### Requirement: Booking

#### Scenario: Car available

- **WHEN** a customer books a car
- **AND** a car of the chosen class is free
- **AND** the customer has a valid driving licence
- **THEN** the system confirms the booking

#### Scenario: No car of the class

- **WHEN** a customer books a car
- **AND** the customer has a valid driving licence
- **AND** no car of the chosen class is free
- **THEN** the system offers a car of a higher class

#### Scenario: No licence

- **WHEN** a customer books a car
- **AND** the customer has no valid driving licence
- **THEN** the system rejects the booking

### Requirement: Return

#### Scenario: Extra day

- **WHEN** a car is returned more than 2 hours after the agreed time or at another branch and the customer did not book a one-way rental
- **THEN** the system charges one extra day

#### Scenario: Damage

- **WHEN** a car is returned with new damage
- **THEN** the system charges the repair costs to the customer
