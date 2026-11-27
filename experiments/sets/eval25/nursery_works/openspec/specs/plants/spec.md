# plants Specification

## Purpose

A sales assistant handles the requests of a plant nursery and calls the tools of the stock system.

## Requirements

### Requirement: Confirmations

A reservation SHALL be confirmed to the customer.

#### Scenario: A reservation is confirmed

- **WHEN** a call of `reserve_plant` succeeds
- **THEN** the customer was sent a confirmation in the run

### Requirement: Price list code

The price list SHALL be built without the mail module.

#### Scenario: The price list does not use the mail module

- **WHEN** a price list is built in a run
- **THEN** the code that builds it does not import the mail module

### Requirement: Watering rounds

A watering round SHALL cover the east house.

#### Scenario: The east house is watered

- **WHEN** a watering round is handled in a run
- **THEN** every bed of the east house is watered in the run

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a plant is reserved

- **WHEN** ilse asks to reserve fern f2
- **THEN** `reserve_plant` is called once
- **AND** the answer gives the pick-up day
