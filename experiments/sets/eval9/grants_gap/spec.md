# Grants Specification

## Purpose

Researchers apply online for small research grants.

## Requirements

### Requirement: Applications

#### Scenario: Complete application

- **WHEN** a researcher submits an application
- **AND** all required documents are attached
- **THEN** the system sends the application to two reviewers

### Requirement: Decisions

#### Scenario: Funding

- **WHEN** the committee approves an application
- **THEN** the system transfers the first payment to the researcher's institution

### Requirement: Reviews

#### Scenario: Late reviewer

- **WHEN** a reviewer misses the review deadline for the second time
- **THEN** the system removes the reviewer from the panel

### Requirement: Reporting

#### Scenario: Final report

- **WHEN** a project ends
- **THEN** the system asks the researcher for a final report
