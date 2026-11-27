## ADDED Requirements

### Requirement: After hours

A car SHALL be handed over after hours without the desk.

#### Scenario: An after-hours run asks nobody

- **WHEN** a call of `ask_desk` is made
- **THEN** the run is not an after-hours run

#### Scenario: After hours the key box is used

- **WHEN** a call of `hand_over_car` succeeds in an after-hours run
- **THEN** the answer gives the key-box code
