# grants Specification

## Purpose

Researchers apply online for small research grants.

## Requirements

### Requirement: Applications

The system SHALL handle applications.

#### Scenario: Complete application

- **WHEN** a researcher submits an application
- **AND** all required documents are attached
- **THEN** the system sends the application to two reviewers

#### Scenario: Incomplete application

- **WHEN** a researcher submits an application
- **AND** a required document is missing
- **THEN** the system returns the application to the researcher

### Requirement: Decisions

The system SHALL handle decisions.

#### Scenario: Funding

- **WHEN** the committee approves an application
- **THEN** the system transfers the first payment to the researcher's institution

### Requirement: Reviews

The system SHALL handle reviews.

#### Scenario: Late reviewer

- **WHEN** a reviewer misses the review deadline for the second time
- **THEN** the system removes the reviewer from the panel

### Requirement: Reporting

The system SHALL handle reporting.

#### Scenario: Final report

- **WHEN** a project ends
- **THEN** the system asks the researcher for a final report
