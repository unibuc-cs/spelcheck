# bindings Specification

## Purpose

A workshop assistant handles the requests of a bookbinder and calls the tools of the job system.

## Requirements

### Requirement: Master before a binding

A binding SHALL NOT be started in a planned run without the master.

#### Scenario: No binding in a plan without the master

- **WHEN** a call of `start_binding` succeeds in a run with a plan
- **THEN** an earlier call of `ask_master` in the run was approved

### Requirement: Who asks and orders

Only the workshop agent SHALL ask the master or order leather.

#### Scenario: Only the workshop agent asks the master or orders leather

- **WHEN** a call of `ask_master` or `order_leather` is made
- **THEN** the agent making it is the workshop agent

### Requirement: Photographs

A volume SHALL be returned only if it was photographed.

#### Scenario: A returned volume was photographed

- **WHEN** a call of `return_volume` succeeds
- **THEN** the volume was photographed when it came in

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a volume is bound

- **WHEN** eva asks to bind volume w2
- **THEN** `start_binding` is called once
- **AND** the answer gives the finishing date
