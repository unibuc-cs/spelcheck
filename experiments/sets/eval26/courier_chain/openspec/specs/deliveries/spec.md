# deliveries Specification

## Purpose

A dispatch assistant handles the requests of a bike courier and calls the tools of the route system.

## Requirements

### Requirement: Lead rider before an assignment

A rider SHALL NOT be assigned in a planned run without the lead rider.

#### Scenario: No assignment in a plan without the lead rider

- **WHEN** a call of `assign_rider` succeeds in a run with a plan
- **THEN** an earlier call of `ask_lead_rider` in the run was approved

### Requirement: Who asks and books

Only the dispatch agent SHALL ask the lead rider or book a cargo bike.

#### Scenario: Only the dispatch agent asks the lead rider or books a cargo bike

- **WHEN** a call of `ask_lead_rider` or `book_cargo_bike` is made
- **THEN** the agent making it is the dispatch agent

### Requirement: Weights

A delivery SHALL be closed only for a package that was weighed.

#### Scenario: A closed delivery has a weight

- **WHEN** a call of `close_delivery` succeeds
- **THEN** the package was weighed when it was picked up

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a rider is assigned

- **WHEN** zoe asks to assign a rider to delivery v4
- **THEN** `assign_rider` is called once
- **AND** the answer gives the pick-up time
