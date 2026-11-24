## MODIFIED Requirements

### Requirement: Check-in

The system SHALL handle check-in.

#### Scenario: Listed visitor

- **WHEN** a visitor checks in at a ward
- **THEN** the system opens the ward door and prints a visitor badge only if the visitor is on the patient's visitor list

#### Scenario: Unlisted visitor

- **WHEN** a visitor checks in at a ward
- **AND** the visitor is not on the patient's visitor list
- **THEN** the system keeps the ward door closed and calls a nurse
