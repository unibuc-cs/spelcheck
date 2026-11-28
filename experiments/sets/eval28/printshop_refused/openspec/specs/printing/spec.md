# printing Specification

## Purpose

A counter assistant handles the requests of a print shop and calls the tools of the job system.

## Requirements

### Requirement: Shop manager before a print

A job SHALL NOT be printed in a planned run without the shop manager.

#### Scenario: No print in a plan without the shop manager

- **WHEN** a call of `print_job` succeeds in a run with a plan
- **THEN** an earlier call of `ask_shop_manager` in the run was approved

### Requirement: Jobs on hold

A job on hold SHALL NOT be printed.

#### Scenario: No print of a job on hold

- **WHEN** any call of `print_job` is made
- **THEN** it never succeeds for a job that is on hold at the start of the run

### Requirement: Proofs

Only a job with a signed proof SHALL be printed.

#### Scenario: A printed job had a signed proof

- **WHEN** any call of `print_job` succeeds
- **THEN** the proof of the job was signed at the start of the run

### Requirement: Telling the customer

A customer who asks for a job on hold SHALL be told.

#### Scenario: A job on hold is named

- **WHEN** a request names a job that is on hold at the start of the run
- **THEN** the answer says that the job is on hold

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a job is printed

- **WHEN** ines asks to print job j21
- **THEN** `print_job` is called once
- **AND** the answer gives the pick-up time
