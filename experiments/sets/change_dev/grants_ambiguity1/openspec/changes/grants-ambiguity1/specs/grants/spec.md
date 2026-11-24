## MODIFIED Requirements

### Requirement: Applications

The system SHALL handle applications.

#### Scenario: Complete application

- **WHEN** a researcher submits an application
- **THEN** the system sends the application to two reviewers only if all required documents are attached

#### Scenario: Incomplete application

- **WHEN** a researcher submits an application
- **AND** a required document is missing
- **THEN** the system returns the application to the researcher
