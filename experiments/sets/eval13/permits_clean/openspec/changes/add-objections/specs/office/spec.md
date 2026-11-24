## ADDED Requirements

### Requirement: Objections

The system SHALL take objections from neighbours.

#### Scenario: Period open

- **WHEN** a neighbour files an objection
- **AND** the objection period is open
- **THEN** the system adds the objection to the case

#### Scenario: Period over

- **WHEN** a neighbour files an objection
- **AND** the objection period is not open
- **THEN** the system rejects the objection and explains why
