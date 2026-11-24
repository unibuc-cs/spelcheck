# harbour Specification

## Purpose

The weather service and the shore power of the harbour.

## Requirements

### Requirement: Weather

The system SHALL pass on storm warnings.

#### Scenario: Storm warning

- **WHEN** a storm warning is in force
- **THEN** the system shows the warning on the harbour screens

### Requirement: Shore power

The system SHALL watch the shore power of the pontoons.

#### Scenario: Third outage

- **WHEN** the shore power of a pontoon fails for the third time in a week
- **THEN** the system calls the electrician
