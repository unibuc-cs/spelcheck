# rentals Specification

## Purpose

A rental assistant handles the requests of a car rental and calls the tools of the fleet system.

## Requirements

### Requirement: Desk before a hand-over

A car SHALL NOT be handed over in a planned run without the desk.

#### Scenario: No hand-over in a plan without the desk

- **WHEN** a call of `hand_over_car` succeeds in a run with a plan
- **THEN** an earlier call of `ask_desk` in the run was approved

### Requirement: Closing a rental

A rental SHALL be closed only for a car that was inspected.

#### Scenario: A closed rental had an inspection

- **WHEN** a call of `close_rental` succeeds
- **THEN** the car was inspected when it was handed over

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a car is handed over

- **WHEN** sofia asks to pick up car v2
- **THEN** `hand_over_car` is called once
- **AND** the answer gives the parking bay
