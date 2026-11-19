# Upload Specification

## Purpose

Users upload documents to a shared folder that has a size limit.

## Requirements

### Requirement: Upload

#### Scenario: Accepted file

- **WHEN** a user uploads a file
- **AND** the file is at most 10 MB
- **AND** the file type is allowed
- **AND** the folder has free space
- **THEN** the system stores the file

#### Scenario: File too large

- **WHEN** a user uploads a file
- **AND** the file is larger than 10 MB
- **THEN** the system rejects the file and shows a size error

#### Scenario: Type not allowed

- **WHEN** a user uploads a file
- **AND** the file type is not allowed
- **THEN** the system rejects the file and shows a type error

### Requirement: Quota

#### Scenario: Folder full

- **WHEN** a user uploads a file
- **AND** the folder has no free space
- **THEN** the system rejects the file

### Requirement: Notification

#### Scenario: Owner notified

- **WHEN** the system stores a file
- **THEN** the system notifies the folder owner

#### Scenario: Silent uploads

- **WHEN** the system stores a file
- **THEN** the system does not notify anyone
