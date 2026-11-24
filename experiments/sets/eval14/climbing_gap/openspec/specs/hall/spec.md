# hall Specification

## Purpose

Courses, fall reports, and the setting of new routes.

## Requirements

### Requirement: Courses

The system SHALL take sign-ups for courses.

#### Scenario: Places left

- **WHEN** a climber signs up for a course
- **AND** places are left
- **THEN** the system adds the climber to the course

#### Scenario: Course full

- **WHEN** a climber signs up for a course
- **AND** no places are left
- **THEN** the system suggests the next course

### Requirement: Fall reports

The system SHALL act on falls that are reported.

#### Scenario: Second fall report

- **WHEN** a route gets a fall report for the second time in a week
- **THEN** the system closes the route for inspection

### Requirement: Route setting

The system SHALL announce the setting of new routes.

#### Scenario: Setting in progress

- **WHEN** routes are being set in the hall
- **THEN** the system shows the closed walls on the screen
