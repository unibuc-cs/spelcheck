# office Specification

## Purpose

Registration, cancellations, and the days on which the cars are serviced.

## Requirements

### Requirement: Registration

The system SHALL register new learners.

#### Scenario: Eye test valid

- **WHEN** a person registers as a learner
- **AND** the eye test of the person is valid
- **THEN** the system creates a learner file

#### Scenario: Eye test not valid

- **WHEN** a person registers as a learner
- **AND** the eye test of the person is not valid
- **THEN** the system asks for a new eye test

### Requirement: Late cancellations

The system SHALL act on lessons that are cancelled late.

#### Scenario: Third late cancellation

- **WHEN** a learner cancels a lesson late for the third time
- **THEN** the system charges the learner for the lesson

### Requirement: Car service

The system SHALL announce the days on which the cars are serviced.

#### Scenario: Service day

- **WHEN** the cars are being serviced
- **THEN** the system shows the service day in the calendar
