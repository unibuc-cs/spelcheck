# screenings Specification

## Purpose

Customers buy seats for film screenings and enter the hall with their ticket.

## Requirements

### Requirement: Seat sale

The system SHALL sell seats for screenings.

#### Scenario: Seats left

- **WHEN** a customer asks for a seat at a screening
- **AND** seats are left for the screening
- **THEN** the system sells the seat and shows its number

#### Scenario: Sold out

- **WHEN** a customer asks for a seat at a screening
- **AND** no seats are left for the screening
- **THEN** the system offers the customer the next screening of the film

### Requirement: Admission

The system SHALL check tickets at the hall door.

#### Scenario: Ticket scan

- **WHEN** a customer scans a ticket at the hall door
- **THEN** the system lets the customer into the hall
