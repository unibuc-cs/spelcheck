# Attendance Specification

## Purpose

Students check in at school with a card; parents are told about absences.

## Requirements

### Requirement: Check-in

#### Scenario: On time

- **WHEN** a student scans the card
- **AND** it is before 8:00
- **THEN** the system records the student as present

#### Scenario: Late

- **WHEN** a student scans the card
- **AND** it is 8:00 or later
- **THEN** the system records the student as late

### Requirement: Absence

#### Scenario: Missing student

- **WHEN** the first lesson ends
- **AND** a student has not scanned the card
- **AND** no illness has been reported for the student
- **THEN** the system records the student as absent and sends a message to the parents

#### Scenario: Illness

- **WHEN** a parent reports an illness
- **THEN** the system records the student as excused

### Requirement: Late arrivals

#### Scenario: Third late arrival

- **WHEN** a student is recorded as late for the third time in a term
- **THEN** the system asks the class teacher to call the parents

### Requirement: Trips

#### Scenario: School trip

- **WHEN** the class of a student is on a school trip
- **THEN** the system records no student of that class as absent
