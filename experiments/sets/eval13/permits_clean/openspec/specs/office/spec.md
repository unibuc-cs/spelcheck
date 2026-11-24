# office Specification

## Purpose

Site visits, old files, and when the permit office holds back.

## Requirements

### Requirement: Site visits

The system SHALL plan site visits.

#### Scenario: Inspector available

- **WHEN** a case officer asks for a site visit
- **AND** an inspector is available that week
- **THEN** the system books the visit and informs the builder

#### Scenario: No inspector

- **WHEN** a case officer asks for a site visit
- **AND** no inspector is available that week
- **THEN** the system puts the visit on the waiting list

### Requirement: Old files

The system SHALL fetch old files on request.

#### Scenario: File requested

- **WHEN** a citizen asks to see an old file
- **THEN** the system orders the file from the archive

### Requirement: Election silence

The system SHALL publish nothing during an election campaign.

#### Scenario: Campaign running

- **WHEN** an election campaign is running
- **THEN** the system does not publish any decision on the notice board

### Requirement: Staff training

The system SHALL announce days on which the office is closed for training.

#### Scenario: Office closed

- **WHEN** the office is closed for staff training
- **THEN** the system shows the closing on the website
