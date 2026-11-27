## ADDED Requirements

### Requirement: Ripe weeks

In a ripe week a crew SHALL be sent without the grower.

#### Scenario: A ripe-week run asks nobody

- **WHEN** a call of `ask_grower` is made
- **THEN** the run is not a ripe-week run

#### Scenario: A ripe-week crew gets its row plan

- **WHEN** a call of `send_crew` succeeds in a ripe-week run
- **THEN** the answer gives the row plan
