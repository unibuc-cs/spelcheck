## ADDED Requirements

### Requirement: Nursery slope

A nursery-slope run SHALL NOT book lift passes.

#### Scenario: A nursery-slope run books no lift pass

- **WHEN** a call of `book_lift_pass` is made
- **THEN** the run is not a nursery-slope run

#### Scenario: A nursery-slope run names the head instructor

- **WHEN** a call of `ask_head_instructor` is made in a nursery-slope run
- **THEN** the answer names the head instructor who was asked
