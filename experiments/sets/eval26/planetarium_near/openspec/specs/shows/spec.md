# shows Specification

## Purpose

A booking assistant handles the requests of a planetarium and calls the tools of the show system.

## Requirements

### Requirement: Astronomer before the dome

The dome SHALL NOT be booked in a planned run without the astronomer.

#### Scenario: No dome in a plan without the astronomer

- **WHEN** a call of `book_dome` succeeds in a run with a plan
- **THEN** an earlier call of `ask_astronomer` in the run was approved

### Requirement: Who asks and rents

Only the booking agent SHALL ask the astronomer or rent a telescope.

#### Scenario: Only the booking agent asks the astronomer or rents a telescope

- **WHEN** a call of `ask_astronomer` or `rent_telescope` is made
- **THEN** the agent making it is the booking agent

### Requirement: Projector

A show SHALL start only with a serviced projector.

#### Scenario: A show needs a serviced projector

- **WHEN** a call of `start_show` succeeds
- **THEN** the projector was serviced before the season

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: the dome is booked

- **WHEN** maja asks to book the dome for class c5
- **THEN** `book_dome` is called once
- **AND** the answer gives the start time
