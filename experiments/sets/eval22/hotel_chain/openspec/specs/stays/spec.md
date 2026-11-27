# stays Specification

## Purpose

A front-desk assistant handles the requests of a hotel and calls the tools of the booking system.

## Requirements

### Requirement: Manager before a check-in

A guest SHALL NOT be checked in in a planned run without the manager.

#### Scenario: No check-in in a plan without the manager

- **WHEN** a call of `check_in_guest` succeeds in a run with a plan
- **THEN** an earlier call of `ask_manager` in the run was approved

### Requirement: Refunds

A stay SHALL be refunded only to a verified card.

#### Scenario: A refund goes to a verified card

- **WHEN** a call of `refund_stay` succeeds
- **THEN** the guest's card was verified at check-in

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a guest is checked in

- **WHEN** lea asks to check in guest g5
- **THEN** `check_in_guest` is called once
- **AND** the answer gives the room number
