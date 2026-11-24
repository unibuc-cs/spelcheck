# entry Specification

## Purpose

Climbers check in at a climbing hall and hand back rental gear.

## Requirements

### Requirement: Entry with a safety check

The system SHALL let in climbers who have passed the safety check.

#### Scenario: Check passed

- **WHEN** a climber checks in
- **AND** the climber has passed the safety check
- **THEN** the system opens the turnstile and counts the visit

### Requirement: Entry without a safety check

The system SHALL send new climbers to an instructor.

#### Scenario: Check missing

- **WHEN** a climber checks in
- **AND** the climber has not passed the safety check
- **THEN** the system sends the climber to the instructor

### Requirement: Rental gear

The system SHALL take back rental gear.

#### Scenario: Gear handed back

- **WHEN** a climber hands back rental gear
- **THEN** the system releases the deposit
