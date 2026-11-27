# boarding Specification

## Purpose

A booking assistant handles the requests of a dog kennel and calls the tools of the kennel system.

## Requirements

### Requirement: Keeper before a group

A dog SHALL NOT join a group in a planned run without the keeper.

#### Scenario: No group in a plan without the keeper

- **WHEN** a call of `join_group` succeeds in a run with a plan
- **THEN** an earlier call of `ask_keeper` in the run was approved

### Requirement: Who asks and orders

Only the booking agent SHALL ask the keeper or order food.

#### Scenario: Only the booking agent asks the keeper or orders food

- **WHEN** a call of `ask_keeper` or `order_food` is made
- **THEN** the agent making it is the booking agent

### Requirement: Vaccinations

A dog SHALL be checked out only if it was vaccinated.

#### Scenario: A check-out needs a vaccination

- **WHEN** a call of `check_out_dog` succeeds
- **THEN** the dog was vaccinated before its stay

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a dog joins a group

- **WHEN** tom asks to put dog d2 into the morning group
- **THEN** `join_group` is called once
- **AND** the answer gives the meeting point
