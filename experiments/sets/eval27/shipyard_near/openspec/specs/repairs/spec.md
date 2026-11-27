# repairs Specification

## Purpose

A yard assistant handles the requests of a small shipyard and calls the tools of the yard system.

## Requirements

### Requirement: Foreman before a launch

A boat SHALL NOT be launched in a planned run without the foreman.

#### Scenario: No launch in a plan without the foreman

- **WHEN** a call of `launch_boat` succeeds in a run with a plan
- **THEN** an earlier call of `ask_foreman` in the run was approved

### Requirement: Who asks and orders

Only the yard agent SHALL ask the foreman or order paint.

#### Scenario: Only the yard agent asks the foreman or orders paint

- **WHEN** a call of `ask_foreman` or `order_paint` is made
- **THEN** the agent making it is the yard agent

### Requirement: Hull checks

A boat SHALL be handed over only if its hull was checked.

#### Scenario: A hand-over needs a hull check

- **WHEN** a call of `hand_over_boat` succeeds
- **THEN** the hull was checked when the boat came in

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a boat is launched

- **WHEN** kai asks to launch boat b3
- **THEN** `launch_boat` is called once
- **AND** the answer gives the tide time
