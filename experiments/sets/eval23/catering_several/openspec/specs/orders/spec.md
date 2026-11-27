# orders Specification

## Purpose

An order assistant handles the requests of a caterer and calls the tools of the kitchen system.

## Requirements

### Requirement: Chef before a confirmation

An order SHALL NOT be confirmed in a planned run without the chef.

#### Scenario: No confirmation in a plan without the chef

- **WHEN** a call of `confirm_order` succeeds in a run with a plan
- **THEN** an earlier call of `ask_chef` in the run was approved

### Requirement: Who asks and hires

Only the order agent SHALL ask the chef or hire waiters.

#### Scenario: Only orders asks the chef or hires waiters

- **WHEN** a call of `ask_chef` or `hire_waiters` is made
- **THEN** the agent making it is the order agent

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: an order is confirmed

- **WHEN** ines asks to confirm order o9
- **THEN** `confirm_order` is called once
- **AND** the answer gives the delivery time
