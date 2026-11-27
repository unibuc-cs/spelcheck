# harvest Specification

## Purpose

A picking assistant handles the requests of a fruit orchard and calls the tools of the harvest system.

## Requirements

### Requirement: Grower before a crew

A crew SHALL NOT be sent in a planned run without the grower.

#### Scenario: No crew in a plan without the grower

- **WHEN** a call of `send_crew` succeeds in a run with a plan
- **THEN** an earlier call of `ask_grower` in the run was approved

### Requirement: Who asks and rents

Only the picking agent SHALL ask the grower or rent a tractor.

#### Scenario: Only the picking agent asks the grower or rents a tractor

- **WHEN** a call of `ask_grower` or `rent_tractor` is made
- **THEN** the agent making it is the picking agent

### Requirement: Grading

Crates SHALL be shipped only with graded fruit.

#### Scenario: Shipped fruit was graded

- **WHEN** a call of `ship_crates` succeeds
- **THEN** the fruit was graded on the day it was picked

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a crew is sent

- **WHEN** bea asks to send a crew to row r6
- **THEN** `send_crew` is called once
- **AND** the answer gives the start time
