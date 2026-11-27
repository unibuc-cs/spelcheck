# visits Specification

## Purpose

A reception assistant handles the requests of a veterinary practice and calls the tools of the practice system.

## Requirements

### Requirement: Vet before an admission

An animal SHALL NOT be admitted in a planned run without the vet.

#### Scenario: No admission in a plan without the vet

- **WHEN** a call of `admit_animal` succeeds in a run with a plan
- **THEN** an earlier call of `ask_vet` in the run was approved

### Requirement: Who asks and orders

Only the reception agent SHALL ask the vet or order medicine.

#### Scenario: Only reception asks the vet or orders medicine

- **WHEN** a call of `ask_vet` or `order_medicine` is made
- **THEN** the agent making it is the reception agent

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: an animal is admitted

- **WHEN** noor asks to admit dog d4
- **THEN** `admit_animal` is called once
- **AND** the answer gives the kennel number
