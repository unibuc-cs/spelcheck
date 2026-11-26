## ADDED Requirements

### Requirement: The night counter

A refill at the night counter SHALL be handed out at once.

#### Scenario: Example: a night-counter refill

- **WHEN** nora sends a night-counter request for prescription p9
- **THEN** `dispense_medicine` succeeds once
- **AND** `verify_prescription` is never called
