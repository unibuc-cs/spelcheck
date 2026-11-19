# Exam Specification

## Purpose

Students take online exams with a time limit; the exams are graded automatically.

## Requirements

### Requirement: Submission

#### Scenario: In time

- **WHEN** a student submits the exam
- **AND** the time limit has not passed
- **THEN** the system records the submission

#### Scenario: Too late

- **WHEN** a student submits the exam
- **AND** the time limit has passed
- **THEN** the system rejects the submission

### Requirement: Grading

#### Scenario: Pass

- **WHEN** a recorded submission is graded
- **THEN** the system shows the score and marks the exam as passed if the score is at least 50 points

#### Scenario: Fail

- **WHEN** a recorded submission is graded
- **AND** the score is below 50 points
- **THEN** the system marks the exam as failed

### Requirement: Retake

#### Scenario: Failed exam

- **WHEN** an exam is marked as failed
- **THEN** the system allows the student one retake
