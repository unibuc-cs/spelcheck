## ADDED Requirements

### Requirement: Paper covers

A paper-cover run SHALL NOT order leather.

#### Scenario: A paper-cover run orders no leather

- **WHEN** a call of `order_leather` is made
- **THEN** the run is not a paper-cover run

#### Scenario: A paper-cover run names the master

- **WHEN** a call of `ask_master` is made in a paper-cover run
- **THEN** the answer names the master who was asked
