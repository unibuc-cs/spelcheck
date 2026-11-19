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

#### Scenario: Licence check

- **WHEN** a customer books a car
- **THEN** the system confirms bookings only for customers with a valid driving licence

### Requirement: Return

#### Scenario: Late return

- **WHEN** a car is returned more than 2 hours after the agreed time
- **THEN** the system charges one extra day

#### Scenario: Damage

- **WHEN** a car is returned with new damage
- **THEN** the system charges the repair costs to the customer
