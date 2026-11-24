# desk Specification

## Purpose

Photos, corrections, and the state of the newsroom and its website.

## Requirements

### Requirement: Photos

The system SHALL find photos for articles.

#### Scenario: Photo in the archive

- **WHEN** an editor asks for a photo
- **AND** a fitting photo is in the archive
- **THEN** the system attaches the photo to the article

#### Scenario: No photo in the archive

- **WHEN** an editor asks for a photo
- **AND** no fitting photo is in the archive
- **THEN** the system sends a request to the photo desk

### Requirement: Corrections

The system SHALL follow up on errors that readers report.

#### Scenario: Error reported

- **WHEN** a reader reports an error in an article
- **THEN** the system opens a correction case for the article

### Requirement: Maintenance

The system SHALL keep the website unchanged during maintenance.

#### Scenario: Maintenance mode

- **WHEN** the website is in maintenance mode
- **THEN** the system does not publish any article on the website

### Requirement: Night hours

The system SHALL tell reporters whom to reach at night.

#### Scenario: No editor on duty

- **WHEN** no editor is on duty
- **THEN** the system shows the night contact to the reporters
