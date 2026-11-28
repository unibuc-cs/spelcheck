## ADDED Requirements

### Requirement: Touring shows

For a touring show an exhibit SHALL be lent without the curator.

#### Scenario: A touring run asks nobody

- **WHEN** a call of `ask_curator` is made
- **THEN** the run is not a touring run

#### Scenario: A touring loan names the crate

- **WHEN** a call of `lend_exhibit` succeeds in a touring run
- **THEN** the answer names the crate
