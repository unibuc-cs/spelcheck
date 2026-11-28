## ADDED Requirements

### Requirement: Swarm days

On a swarm day a hive SHALL be moved without the beekeeper.

#### Scenario: A swarm-day run asks nobody

- **WHEN** a call of `ask_beekeeper` is made
- **THEN** the run is not a swarm-day run

#### Scenario: A swarm-day move names the stand

- **WHEN** a call of `move_hive` succeeds in a swarm-day run
- **THEN** the answer names the stand
