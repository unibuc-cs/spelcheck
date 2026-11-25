# Issues Specification

## Purpose

A tracker keeps the issues of a software project.

## Requirements

### Requirement: Triage

#### Scenario: Reproduced

- **WHEN** a maintainer triages an issue
- **AND** the issue can be reproduced
- **THEN** the tracker sets the state of the issue to `in review`
- **AND** assigns the issue to the maintainer

#### Scenario: Not reproduced

- **WHEN** a maintainer triages an issue
- **AND** the issue cannot be reproduced
- **THEN** the tracker sets the state of the issue to `needs info`
- **AND** asks the reporter for steps

### Requirement: Closing

#### Scenario: Fix merged

- **WHEN** a maintainer closes an issue
- **AND** a fix is merged
- **THEN** the tracker sets the state of the issue to `done`
- **AND** adds the issue to the release notes

#### Scenario: No fix merged

- **WHEN** a maintainer closes an issue
- **AND** no fix is merged
- **THEN** the tracker sets the state of the issue to `not planned`

### Requirement: Labels

#### Scenario: Known label

- **WHEN** a member adds a label
- **AND** the label is one of `kind:bug`, `kind:feature` or `kind:docs`
- **THEN** the tracker shows the label on the issue

#### Scenario: Unknown label

- **WHEN** a member adds a label
- **AND** the label is not one of `kind:bug`, `kind:feature` or `kind:docs`
- **THEN** the tracker answers with status 422

### Requirement: Reopening

#### Scenario: Closed recently

- **WHEN** the reporter reopens an issue
- **AND** the issue was closed less than 30 days ago
- **THEN** the tracker sets the state of the issue to `in review`

#### Scenario: Closed long ago

- **WHEN** the reporter reopens an issue
- **AND** the issue was not closed less than 30 days ago
- **THEN** the tracker asks the reporter to open a new issue

### Requirement: Search

#### Scenario: Issues listed

- **WHEN** a member searches the issues
- **THEN** the tracker lists the matching issues with their state

### Requirement: Spam

#### Scenario: Third report

- **WHEN** an account is reported for spam for the third time
- **THEN** the tracker blocks the account
