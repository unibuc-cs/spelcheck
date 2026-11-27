## ADDED Requirements

### Requirement: Regulars

A regular guest SHALL join a group without the keeper.

#### Scenario: A regulars run asks nobody

- **WHEN** a call of `ask_keeper` is made
- **THEN** the run is not a regulars run

#### Scenario: A regular gets its usual group

- **WHEN** a call of `join_group` succeeds in a regulars run
- **THEN** the answer names the dog's usual group
