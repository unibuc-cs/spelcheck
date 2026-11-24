## ADDED Requirements

### Requirement: Registered mail

The system SHALL tell students about registered mail.

#### Scenario: Student in the house

- **WHEN** registered mail arrives for a student
- **AND** the student is in the house
- **THEN** the system informs the student at once

#### Scenario: Student away

- **WHEN** registered mail arrives for a student
- **AND** the student is not in the house
- **THEN** the system keeps the mail at the desk and sends an email
