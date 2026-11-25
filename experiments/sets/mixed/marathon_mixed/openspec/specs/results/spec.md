# results Specification

## Purpose

Times, rankings and certificates after the race.

## Requirements

### Requirement: Finish times

The system SHALL publish the times of the runners.

#### Scenario: Runner finishes

- **WHEN** a runner crosses the finish line
- **THEN** the system publishes the finish time of the runner

### Requirement: Protests

The system SHALL hold back results that are under protest.

#### Scenario: Protest open

- **WHEN** a protest against a result is open
- **THEN** the system does not publish any finish time

### Requirement: Certificates

The system SHALL send certificates to runners.

#### Scenario: Result final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is final
- **THEN** the system sends the certificate by email

#### Scenario: Result not final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is not final
- **THEN** the system tells the runner the date of the final results

### Requirement: Age groups

The system SHALL rank the runners.

#### Scenario: Results final

- **WHEN** the results of the race are final
- **THEN** the system ranks the runners in their age groups

### Requirement: Disqualification

The system SHALL act on the warnings of the referees.

#### Scenario: Third warning

- **WHEN** a runner receives a warning from a referee for the third time
- **THEN** the system disqualifies the runner

### Requirement: Photos

The system SHALL give runners their finish photo.

#### Scenario: Photo available

- **WHEN** a runner asks for the finish photo
- **AND** the photo is available
- **THEN** the system sends the runner a link to the photo

#### Scenario: Photo not available

- **WHEN** a runner asks for the finish photo
- **AND** the photo is not available
- **THEN** the system tells the runner when the photos will be ready

### Requirement: Records

The system SHALL announce records.

#### Scenario: Course record

- **WHEN** the finish time of a runner is below the course record
- **THEN** the system announces a new course record

### Requirement: Corrections

The system SHALL tell runners when their time is corrected.

#### Scenario: Time corrected

- **WHEN** a referee corrects a finish time
- **THEN** the system informs the runner of the new time
