# Photos Specification

## Purpose

Users upload photos to albums and share them with friends.

## Requirements

### Requirement: Upload

#### Scenario: Photo uploaded

- **WHEN** a user uploads a photo
- **AND** the photo is smaller than 20 MB
- **THEN** the system adds the photo to the album

#### Scenario: Photo too large

- **WHEN** a user uploads a photo
- **AND** the photo is 20 MB or larger
- **THEN** the system rejects the photo

### Requirement: Sharing

#### Scenario: Album shared

- **WHEN** a user shares an album with a friend
- **THEN** the system sends the friend a link only if the friend has an account

### Requirement: Deleting

#### Scenario: Photo deleted

- **WHEN** a user deletes a photo
- **THEN** the system erases the photo

### Requirement: Logging

#### Scenario: Upload log

- **WHEN** a user uploads a photo
- **THEN** the system writes an entry to the upload log and keeps the entry for one year
