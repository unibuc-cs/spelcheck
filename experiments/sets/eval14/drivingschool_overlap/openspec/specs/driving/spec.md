# driving Specification

## Purpose

Learners of a driving school book lessons and take the theory test.

## Requirements

### Requirement: Lessons with a free car

The system SHALL book a lesson when a car is free.

#### Scenario: Car free

- **WHEN** a learner books a driving lesson
- **AND** a car is free at that time
- **THEN** the system books the lesson and assigns a car

### Requirement: Lessons without a free car

The system SHALL offer another time when no car is free.

#### Scenario: No car free

- **WHEN** a learner books a driving lesson
- **AND** no car is free at that time
- **THEN** the system offers the learner another time

### Requirement: Theory test

The system SHALL record the result of the theory test.

#### Scenario: Test passed

- **WHEN** a learner passes the theory test
- **THEN** the system opens the booking of road lessons for the learner
