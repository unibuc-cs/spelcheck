# school Specification

## Purpose

Instruments on loan, absences, and school concerts.

## Requirements

### Requirement: Instrument loans

The system SHALL lend instruments to pupils.

#### Scenario: Instrument on the shelf

- **WHEN** a pupil asks to borrow an instrument
- **AND** the instrument is on the shelf
- **THEN** the system records the loan

#### Scenario: Instrument lent out

- **WHEN** a pupil asks to borrow an instrument
- **AND** the instrument is not on the shelf
- **THEN** the system reserves the instrument for the pupil

### Requirement: Absences

The system SHALL tell the parents about missed lessons.

#### Scenario: Third absence

- **WHEN** a pupil misses a lesson for the third time in a term
- **THEN** the system informs the parents

### Requirement: Concerts

The system SHALL announce school concerts.

#### Scenario: Concert evening

- **WHEN** a school concert is taking place
- **THEN** the system shows the programme in the hall
