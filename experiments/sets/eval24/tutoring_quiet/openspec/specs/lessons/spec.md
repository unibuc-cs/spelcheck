# lessons Specification

## Purpose

A booking assistant handles the requests of a tutoring school and calls the tools of the timetable system.

## Requirements

### Requirement: Head teacher before a group change

A pupil SHALL NOT change groups in a planned run without the head teacher.

#### Scenario: No group change in a plan without the head teacher

- **WHEN** a call of `change_group` succeeds in a run with a plan
- **THEN** an earlier call of `ask_head_teacher` in the run was approved

### Requirement: Parents are told

Parents SHALL be told about every group change and every cancelled lesson.

#### Scenario: Group changes and cancellations reach the parents

- **WHEN** a call of `change_group` or `cancel_lesson` is made
- **THEN** the run sends a message to the parents

### Requirement: Rooms

A room SHALL be booked, swapped or released only in term time.

#### Scenario: Room changes need term time

- **WHEN** a call of `book_room`, `swap_room` or `release_room` is made
- **THEN** the date is in term time

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a group is changed

- **WHEN** lena asks to move pupil p6 to the Tuesday group
- **THEN** `change_group` is called once
- **AND** the answer gives the first lesson
