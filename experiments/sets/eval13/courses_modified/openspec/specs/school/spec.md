# school Specification

## Purpose

Lessons, certificates, and what the school announces.

## Requirements

### Requirement: Missed lessons

The system SHALL handle lessons that a student cannot attend.

#### Scenario: Notice in time

- **WHEN** a student cancels a lesson
- **AND** the lesson is more than 24 hours away
- **THEN** the system offers a replacement lesson

#### Scenario: Late notice

- **WHEN** a student cancels a lesson
- **AND** the lesson is not more than 24 hours away
- **THEN** the system counts the lesson as taken

### Requirement: Certificates

The system SHALL issue certificates.

#### Scenario: Course completed

- **WHEN** a student completes a course
- **THEN** the system issues a certificate of attendance

### Requirement: Audit

The system SHALL freeze the books during an audit.

#### Scenario: Audit running

- **WHEN** the accounts of the school are being audited
- **THEN** the system does not issue any receipt

### Requirement: Teacher absence

The system SHALL announce lessons that do not take place.

#### Scenario: Teacher ill

- **WHEN** a teacher is ill
- **THEN** the system shows the cancelled lessons in the app
