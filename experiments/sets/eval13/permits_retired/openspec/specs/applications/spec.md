# applications Specification

## Purpose

Builders apply for building permits and get a decision.

## Requirements

### Requirement: Complete applications

The system SHALL take in complete applications.

#### Scenario: All plans attached

- **WHEN** a builder submits an application
- **AND** all plans are attached
- **THEN** the system registers the application and assigns a case officer

### Requirement: Incomplete applications

The system SHALL send back incomplete applications.

#### Scenario: Plans missing

- **WHEN** a builder submits an application
- **AND** not all plans are attached
- **THEN** the system returns the application to the builder

### Requirement: Decisions

The system SHALL make decisions known.

#### Scenario: Permit granted

- **WHEN** a case officer decides an application
- **AND** the permit is granted
- **THEN** the system publishes the decision on the notice board

#### Scenario: Permit refused

- **WHEN** a case officer decides an application
- **AND** the permit is not granted
- **THEN** the system sends the reasons to the builder
