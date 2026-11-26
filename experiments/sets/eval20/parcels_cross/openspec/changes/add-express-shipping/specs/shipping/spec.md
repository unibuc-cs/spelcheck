## ADDED Requirements

### Requirement: Express shipping

An express request SHALL ship at once, and nobody is asked.

#### Scenario: An express run asks nobody

- **WHEN** an express request is handled in a run
- **THEN** `request_signoff` is not called in the run

#### Scenario: Example: three express parcels

- **WHEN** dana sends an express request for the parcels k1, k2 and k3
- **THEN** the plan is written once
- **AND** `ship_parcel` succeeds three times
