## ADDED Requirements

### Requirement: Show runs

A show run SHALL NOT service the projector.

#### Scenario: A show run services no projector

- **WHEN** a call of `service_projector` is made
- **THEN** the run is not a show run

#### Scenario: A show run gives the seat count

- **WHEN** a call of `start_show` succeeds in a show run
- **THEN** the answer gives the number of seats
