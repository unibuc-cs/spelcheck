# boarding Specification

## Purpose

A terminal assistant handles the requests of a ferry terminal and calls the tools of the boarding system.

## Requirements

### Requirement: Harbour master before a boarding

A vehicle SHALL NOT be boarded in a planned run without the harbour master.

#### Scenario: No boarding in a plan without the harbour master

- **WHEN** a call of `board_vehicle` succeeds in a run with a plan
- **THEN** an earlier call of `ask_harbour_master` in the run was approved

### Requirement: Flagged vehicles

A vehicle that customs has flagged SHALL NOT be boarded.

#### Scenario: No boarding of a flagged vehicle

- **WHEN** any call of `board_vehicle` is made
- **THEN** it never succeeds for a vehicle that is flagged by customs at the start of the run

### Requirement: Check-in

Only a vehicle that was checked in SHALL be boarded.

#### Scenario: A boarded vehicle was checked in

- **WHEN** any call of `board_vehicle` succeeds
- **THEN** the vehicle was checked in at the start of the run

### Requirement: Telling the driver

The driver of a flagged vehicle SHALL be told.

#### Scenario: A flagged vehicle is named

- **WHEN** a request names a vehicle that is flagged by customs at the start of the run
- **THEN** the answer says that the vehicle is flagged

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a vehicle is boarded

- **WHEN** lena asks to board vehicle v4
- **THEN** `board_vehicle` is called once
- **AND** the answer gives the lane
