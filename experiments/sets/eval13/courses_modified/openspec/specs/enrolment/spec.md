# enrolment Specification

## Purpose

People enrol in the courses of a language school and pay for them.

## Requirements

### Requirement: Enrolment with a test

The system SHALL place people by their test result.

#### Scenario: Test taken

- **WHEN** a person enrols in a course
- **AND** the person has taken the placement test
- **THEN** the system assigns the person to a group and sends the timetable

### Requirement: Enrolment without a test

The system SHALL ask new people to take the placement test.

#### Scenario: Test not taken

- **WHEN** a person enrols in a course
- **AND** the person has not taken the placement test
- **THEN** the system books a placement test for the person

### Requirement: Course fees

The system SHALL collect the course fee.

#### Scenario: Card accepted

- **WHEN** a student pays the course fee
- **AND** the card is accepted
- **THEN** the system issues a receipt

#### Scenario: Card declined

- **WHEN** a student pays the course fee
- **AND** the card is not accepted
- **THEN** the system asks for another means of payment
