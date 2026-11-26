## ADDED Requirements

### Requirement: Other cases of watering

The assistant SHALL handle the cases below as described.

#### Scenario: Example: rain is forecast

- **WHEN** the same request runs while rain is forecast for f3
- **THEN** `open_valve` is never called
- **AND** the answer gives the forecast

#### Scenario: Example: a second pass is planned

- **WHEN** the same request runs and iris asks for a second pass in the evening
- **THEN** `open_valve` is called once
- **AND** `schedule_pass` is called once after it
