## ADDED Requirements

### Requirement: Rush hour

In rush hour a rider SHALL be assigned without the lead rider.

#### Scenario: A rush-hour run asks nobody

- **WHEN** a call of `ask_lead_rider` is made
- **THEN** the run is not a rush-hour run

#### Scenario: A rush-hour delivery names the route

- **WHEN** a call of `assign_rider` succeeds in a rush-hour run
- **THEN** the answer gives the route
