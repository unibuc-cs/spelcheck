## ADDED Requirements

### Requirement: Night sailings

On a night sailing a vehicle SHALL be boarded without the harbour master.

#### Scenario: A night run asks nobody

- **WHEN** a call of `ask_harbour_master` is made
- **THEN** the run is not a night run

#### Scenario: A night boarding names the deck

- **WHEN** a call of `board_vehicle` succeeds in a night run
- **THEN** the answer names the deck
