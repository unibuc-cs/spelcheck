## MODIFIED Requirements

### Requirement: Certificates

The system SHALL send certificates to runners.

#### Scenario: Result final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is final
- **THEN** the system sends the certificate by email and adds the split times

#### Scenario: Result not final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is not final
- **THEN** the system tells the runner the date of the final results

## RENAMED Requirements

- FROM: `### Requirement: Corrections`
- TO: `### Requirement: Time corrections`
