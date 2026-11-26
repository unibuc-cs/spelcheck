# lab-runs Specification

## Purpose

A lab assistant plans the processing of samples and calls the tools of the instruments.

## Requirements

### Requirement: Rack size

The setting `lab.max_tubes` MUST be 24.

#### Scenario: The rack size is configured

- **WHEN** the configuration is checked
- **THEN** `lab.max_tubes` is the integer 24

### Requirement: Supervisor before the centrifuge

The centrifuge SHALL NOT be started in a planned run without the supervisor.

#### Scenario: No spin in a plan without the supervisor

- **WHEN** a call of `start_centrifuge` succeeds in a run with a plan
- **THEN** an earlier call of `ask_supervisor` in the run was approved

### Requirement: Refusal

A supervisor who refuses SHALL stop the plan.

#### Scenario: A refusal stops the plan

- **WHEN** a call of `ask_supervisor` returns a refusal
- **THEN** no call of `start_centrifuge` is made after it in the run

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a labelled tube

- **WHEN** ines asks to weigh tube t4
- **AND** t4 has a label
- **THEN** `weigh_tube` is called once for t4
- **AND** the answer gives the weight

#### Scenario: Example: the label is missing

- **WHEN** the same request runs while t4 has no label
- **THEN** `weigh_tube` is never called
- **AND** the answer asks for the label
