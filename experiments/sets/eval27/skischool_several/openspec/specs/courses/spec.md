# courses Specification

## Purpose

A desk assistant handles the requests of a ski school and calls the tools of the course system.

## Requirements

### Requirement: Head instructor before a move

A pupil SHALL NOT be moved in a planned run without the head instructor.

#### Scenario: No move in a plan without the head instructor

- **WHEN** a call of `move_pupil` succeeds in a run with a plan
- **THEN** an earlier call of `ask_head_instructor` in the run was approved

### Requirement: Who asks and books

Only the desk agent SHALL ask the head instructor or book a lift pass.

#### Scenario: Only the desk agent asks the head instructor or books a lift pass

- **WHEN** a call of `ask_head_instructor` or `book_lift_pass` is made
- **THEN** the agent making it is the desk agent

### Requirement: Tests

A certificate SHALL be issued only to a pupil who passed the test.

#### Scenario: A certificate needs a passed test

- **WHEN** a call of `issue_certificate` succeeds
- **THEN** the pupil passed the test at the end of the course

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a pupil is moved

- **WHEN** jon asks to move pupil s9 to the blue group
- **THEN** `move_pupil` is called once
- **AND** the answer gives the meeting point
