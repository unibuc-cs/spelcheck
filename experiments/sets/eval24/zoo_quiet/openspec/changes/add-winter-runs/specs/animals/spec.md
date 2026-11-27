## ADDED Requirements

### Requirement: Winter runs

A winter run SHALL NOT lock enclosures.

#### Scenario: A winter run locks no enclosure

- **WHEN** a call of `lock_enclosure` is made
- **THEN** the run is not a winter run

#### Scenario: A winter run names the curator

- **WHEN** a call of `ask_curator` is made in a winter run
- **THEN** the answer names the curator who was asked
