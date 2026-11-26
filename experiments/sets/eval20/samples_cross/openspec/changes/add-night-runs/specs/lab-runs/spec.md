## ADDED Requirements

### Requirement: Night runs

A night run SHALL spin at once, and no supervisor is asked.

#### Scenario: A night run asks nobody

- **WHEN** a night request is handled in a run
- **THEN** `ask_supervisor` is not called in the run

#### Scenario: Example: two racks at night

- **WHEN** ines sends a night request for the racks r1 and r2
- **THEN** the plan is written once
- **AND** `start_centrifuge` succeeds twice
