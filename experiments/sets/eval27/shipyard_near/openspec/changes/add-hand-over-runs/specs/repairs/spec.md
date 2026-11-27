## ADDED Requirements

### Requirement: Hand-over runs

A hand-over run SHALL NOT check hulls.

#### Scenario: A hand-over run checks no hull

- **WHEN** a call of `check_hull` is made
- **THEN** the run is not a hand-over run

#### Scenario: A hand-over run gives the invoice

- **WHEN** a call of `hand_over_boat` succeeds in a hand-over run
- **THEN** the answer gives the invoice number
