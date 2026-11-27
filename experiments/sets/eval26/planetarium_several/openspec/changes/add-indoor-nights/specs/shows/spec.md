## ADDED Requirements

### Requirement: Indoor nights

An indoor night SHALL NOT rent a telescope.

#### Scenario: An indoor-night run rents no telescope

- **WHEN** a call of `rent_telescope` is made
- **THEN** the run is not an indoor-night run

#### Scenario: An indoor night names the astronomer

- **WHEN** a call of `ask_astronomer` is made in an indoor-night run
- **THEN** the answer names the astronomer who was asked
