# lending Specification

## Purpose

A lending assistant handles the requests of a credit union and calls the tools of the loan system.

## Requirements

### Requirement: Officer before a payout

A loan SHALL NOT be paid out in a planned run without the credit officer.

#### Scenario: No payout in a plan without the officer

- **WHEN** a call of `pay_out_loan` succeeds in a run with a plan
- **THEN** an earlier call of `ask_officer` in the run was approved

### Requirement: Who asks and checks

Only the lending agent SHALL ask the officer or request a credit report.

#### Scenario: Only lending asks the officer or requests a report

- **WHEN** a call of `ask_officer` or `request_report` is made
- **THEN** the agent making it is the lending agent

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a loan is paid out

- **WHEN** tomas asks to pay out loan l2
- **THEN** `pay_out_loan` is called once
- **AND** the answer gives the payout date
