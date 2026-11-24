# donors Specification

## Purpose

Donors check in to give blood and hear about their test results.

## Requirements

### Requirement: Donors who may give

The system SHALL admit donors who may give blood.

#### Scenario: Last donation long ago

- **WHEN** a donor checks in
- **AND** the last donation of the donor is more than 8 weeks ago
- **THEN** the system prints a donation form and calls the donor

### Requirement: Donors who must wait

The system SHALL turn away donors who gave blood recently.

#### Scenario: Last donation recent

- **WHEN** a donor checks in
- **AND** the last donation of the donor is not more than 8 weeks ago
- **THEN** the system tells the donor the next possible date

### Requirement: Test results

The system SHALL tell donors their test results.

#### Scenario: Normal result

- **WHEN** a test result arrives
- **AND** the result is normal
- **THEN** the system sends the donor a letter of thanks

#### Scenario: Abnormal result

- **WHEN** a test result arrives
- **AND** the result is not normal
- **THEN** the system asks the donor to call the doctor
