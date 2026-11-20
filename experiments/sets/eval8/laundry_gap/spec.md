# Laundry Specification

## Purpose

Residents book and pay for the washing machines in the shared laundry room.

## Requirements

### Requirement: Booking

#### Scenario: Free slot

- **WHEN** a resident books a time slot
- **AND** the slot is free
- **THEN** the system reserves the slot for the resident

### Requirement: Washing

#### Scenario: Start

- **WHEN** a resident starts a machine
- **THEN** the system charges the price of the programme to the resident's account

### Requirement: Booking

#### Scenario: Cancelling

- **WHEN** a resident cancels a booking more than one hour before the slot starts
- **THEN** the system frees the slot

#### Scenario: No-show

- **WHEN** a resident misses a booked slot for the third time in a month
- **THEN** the system notifies the caretaker
