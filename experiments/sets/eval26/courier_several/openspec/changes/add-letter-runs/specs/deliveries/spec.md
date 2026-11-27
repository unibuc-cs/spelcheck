## ADDED Requirements

### Requirement: Letter runs

A letter run SHALL NOT book a cargo bike.

#### Scenario: A letter run books no cargo bike

- **WHEN** a call of `book_cargo_bike` is made
- **THEN** the run is not a letter run

#### Scenario: A letter run names the lead rider

- **WHEN** a call of `ask_lead_rider` is made in a letter run
- **THEN** the answer names the lead rider who was asked
