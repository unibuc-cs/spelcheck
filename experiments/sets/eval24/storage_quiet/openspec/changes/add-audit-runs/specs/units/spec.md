## ADDED Requirements

### Requirement: Audit runs

An audit run SHALL NOT extend codes.

#### Scenario: An audit run extends no code

- **WHEN** a call of `extend_code` is made
- **THEN** the run is not an audit run

#### Scenario: An audit run names the manager

- **WHEN** a call of `ask_site_manager` is made in an audit run
- **THEN** the answer names the manager who was asked
