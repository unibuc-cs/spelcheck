# booking Specification

## Purpose

A travel assistant plans trips for the staff of a company and calls the tools of a booking system.

## Requirements

### Requirement: Budget

The setting `travel.max_nights` MUST be 14.

#### Scenario: The night limit is configured

- **WHEN** the configuration is checked
- **THEN** `travel.max_nights` is the integer 14

### Requirement: Confirmation before paying

A trip SHALL NOT be paid in a planned run without a confirmation of the traveller.

#### Scenario: No payment in a plan without a confirmation

- **WHEN** a call of `pay_booking` succeeds in a run with a plan
- **THEN** an earlier call of `ask_traveller` in the run was answered with yes

### Requirement: Refusal

A traveller who says no SHALL stop the plan.

#### Scenario: A no stops the plan

- **WHEN** a call of `ask_traveller` is answered with no
- **THEN** no call of `pay_booking` is made after it in the run

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a flight with seats

- **WHEN** omar asks for a flight to Lyon on Monday
- **AND** the flight has free seats
- **THEN** `hold_seat` is called once
- **AND** the answer gives the price

#### Scenario: Example: the flight is full

- **WHEN** the same request runs while the flight has no free seats
- **THEN** `hold_seat` is never called
- **AND** the answer offers the next flight
