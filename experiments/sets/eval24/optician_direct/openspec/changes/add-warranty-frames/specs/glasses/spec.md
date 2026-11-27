## ADDED Requirements

### Requirement: Warranty frames

A warranty frame SHALL be replaced without paperwork.

#### Scenario: A warranty run writes no audit entry for a frame

- **WHEN** a call of `order_frame` is made in a warranty run
- **THEN** the run writes no audit entry

#### Scenario: A warranty frame names its case

- **WHEN** a call of `order_frame` succeeds in a warranty run
- **THEN** the answer gives the warranty number
