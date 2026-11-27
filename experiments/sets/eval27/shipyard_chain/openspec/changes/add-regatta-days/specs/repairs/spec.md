## ADDED Requirements

### Requirement: Regatta days

On a regatta day a boat SHALL be launched without the foreman.

#### Scenario: A regatta run asks nobody

- **WHEN** a call of `ask_foreman` is made
- **THEN** the run is not a regatta run

#### Scenario: A regatta launch names the slipway

- **WHEN** a call of `launch_boat` succeeds in a regatta run
- **THEN** the answer gives the slipway
