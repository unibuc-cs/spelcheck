## MODIFIED Requirements

### Requirement: Test results

The system SHALL tell donors their test results.

#### Scenario: Normal result

- **WHEN** a test result arrives
- **AND** the result is normal
- **THEN** the system sends the donor a letter of thanks

#### Scenario: Abnormal result

- **WHEN** a test result arrives
- **AND** the result is not normal
- **THEN** the system asks the donor to call the doctor and blocks further donations
