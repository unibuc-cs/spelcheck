# lessons Specification

## Purpose

Pupils of a music school take lessons and practise in the rooms of the school.

## Requirements

### Requirement: Lessons with a free teacher

The system SHALL book a lesson when a teacher is free.

#### Scenario: Teacher free

- **WHEN** a pupil asks for a lesson
- **AND** a teacher of the instrument is free
- **THEN** the system books the lesson and informs the teacher

### Requirement: Lessons without a free teacher

The system SHALL keep a waiting list for lessons.

#### Scenario: No teacher free

- **WHEN** a pupil asks for a lesson
- **AND** no teacher of the instrument is free
- **THEN** the system puts the pupil on the waiting list

### Requirement: Practice rooms

The system SHALL open the practice rooms to pupils.

#### Scenario: Pupil card

- **WHEN** a pupil holds the card to a practice room
- **THEN** the system unlocks the practice room
