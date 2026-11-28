## ADDED Requirements

### Requirement: Election weeks

In an election week a job SHALL be printed without the shop manager.

#### Scenario: An election-week run asks nobody

- **WHEN** a call of `ask_shop_manager` is made
- **THEN** the run is not an election-week run

#### Scenario: An election-week print names the press

- **WHEN** a call of `print_job` succeeds in an election-week run
- **THEN** the answer names the press
