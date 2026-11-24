# building Specification

## Purpose

Services of the building that all members share.

## Requirements

### Requirement: Post

The system SHALL tell members about their post.

#### Scenario: Parcel arrives

- **WHEN** a parcel arrives for a member
- **THEN** the system sends the member a message

### Requirement: Cleaning

The system SHALL announce the weekly deep cleaning.

#### Scenario: Cleaning in progress

- **WHEN** the weekly deep cleaning is in progress
- **THEN** the system shows a notice on the screens

### Requirement: Printer

The system SHALL keep the shared printer working.

#### Scenario: Third paper jam

- **WHEN** the printer reports a paper jam for the third time in a day
- **THEN** the system calls the service company
