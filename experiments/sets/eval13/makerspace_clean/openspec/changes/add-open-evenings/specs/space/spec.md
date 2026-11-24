## ADDED Requirements

### Requirement: Open evenings

The system SHALL take sign-ups for open evenings.

#### Scenario: Places left

- **WHEN** a guest signs up for an open evening
- **AND** places are left
- **THEN** the system confirms the place by email

#### Scenario: Evening full

- **WHEN** a guest signs up for an open evening
- **AND** no places are left
- **THEN** the system offers the guest the next open evening
