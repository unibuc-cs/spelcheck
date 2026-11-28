# loans Specification

## Purpose

A loans assistant handles the requests of a museum and calls the tools of the collection system.

## Requirements

### Requirement: Curator before a loan

An exhibit SHALL NOT be lent in a planned run without the curator.

#### Scenario: No loan in a plan without the curator

- **WHEN** a call of `lend_exhibit` succeeds in a run with a plan
- **THEN** an earlier call of `ask_curator` in the run was approved

### Requirement: Exhibits under restoration

An exhibit under restoration SHALL NOT be lent.

#### Scenario: No loan of an exhibit under restoration

- **WHEN** any call of `lend_exhibit` is made
- **THEN** it never succeeds for an exhibit that is under restoration at the start of the run

### Requirement: Depot

Only an exhibit from the depot SHALL be lent.

#### Scenario: A lent exhibit was in the depot

- **WHEN** any call of `lend_exhibit` succeeds
- **THEN** the exhibit was in the depot at the start of the run

### Requirement: Telling the borrower

A borrower who asks for an exhibit under restoration SHALL be told.

#### Scenario: An exhibit under restoration is named

- **WHEN** a request names an exhibit that is under restoration at the start of the run
- **THEN** the answer says that the exhibit is under restoration

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: an exhibit is lent

- **WHEN** omar asks to lend exhibit x12
- **THEN** `lend_exhibit` is called once
- **AND** the answer gives the return date
