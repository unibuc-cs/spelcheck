## ADDED Requirements

### Requirement: Replicas

A replica SHALL be lent for a month.

#### Scenario: Example: a replica

- **WHEN** omar sends a replica request for exhibit x17
- **THEN** `lend_exhibit` succeeds once
- **AND** the answer gives a return date one month later
