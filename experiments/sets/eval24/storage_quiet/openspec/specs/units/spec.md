# units Specification

## Purpose

A front-office assistant handles the requests of a self-storage site and calls the tools of the unit system.

## Requirements

### Requirement: Manager before a clearance

A unit SHALL NOT be cleared in a planned run without the site manager.

#### Scenario: No clearance in a plan without the manager

- **WHEN** a call of `clear_unit` succeeds in a run with a plan
- **THEN** an earlier call of `ask_site_manager` in the run was approved

### Requirement: Notices

Every clearance and every lock change SHALL be announced.

#### Scenario: Clearances and lock changes are announced

- **WHEN** a call of `clear_unit` or `change_lock` is made
- **THEN** the run sends a notice to the tenant

### Requirement: Access codes

An access code SHALL be changed only for a unit that is paid up.

#### Scenario: Code changes need a paid unit

- **WHEN** a call of `issue_code`, `reset_code` or `extend_code` is made
- **THEN** the rent of the unit is paid

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a unit is cleared

- **WHEN** petra asks to clear unit u5
- **THEN** `clear_unit` is called once
- **AND** the answer gives the clearance date
