# jobs Specification

## Purpose

A booking assistant handles the requests of a moving company and calls the tools of the dispatch system.

## Requirements

### Requirement: Dispatcher before a truck

A truck SHALL NOT be sent in a planned run without the dispatcher.

#### Scenario: No truck in a plan without the dispatcher

- **WHEN** a call of `send_truck` succeeds in a run with a plan
- **THEN** an earlier call of `ask_dispatcher` in the run was approved

### Requirement: Who asks and rents

Only the booking agent SHALL ask the dispatcher or rent a lift.

#### Scenario: Only booking asks the dispatcher or rents a lift

- **WHEN** a call of `ask_dispatcher` or `rent_lift` is made
- **THEN** the agent making it is the booking agent

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a truck is sent

- **WHEN** omar asks to move flat f6
- **THEN** `send_truck` is called once
- **AND** the answer gives the arrival time
