# Photos Specification

## Purpose

A command-line tool, `pho`, keeps the photos of a family in albums.

## Requirements

### Requirement: Import

#### Scenario: New photo

- **WHEN** the user runs `pho import <file>`
- **AND** the photo is not in the archive
- **THEN** the tool copies the photo into the archive
- **AND** prints the id of the photo

#### Scenario: Known photo

- **WHEN** the user runs `pho import <file>`
- **AND** the photo is already in the archive
- **THEN** the tool copies nothing
- **AND** prints "already imported"

### Requirement: Export

#### Scenario: Album exists

- **WHEN** the user runs `pho export <album>`
- **AND** the album exists
- **THEN** the tool writes a zip file of the album
- **AND** exits with code 0

#### Scenario: Album missing

- **WHEN** the user runs `pho export <album>`
- **AND** the album does not exist
- **THEN** the tool prints "no such album"
- **AND** exits with code 3

### Requirement: Tags

#### Scenario: Tag added

- **WHEN** the user runs `pho tag <photo> <word>`
- **THEN** the tool adds the word to the tags of the photo

### Requirement: Sharing

#### Scenario: Album shared

- **WHEN** the user runs `pho share <album>`
- **THEN** the tool creates a public link for the album

### Requirement: Thumbnail

#### Scenario: Empty album

- **WHEN** an album has no photos
- **THEN** the tool sets the thumbnail of the album to `placeholder`

#### Scenario: Video first

- **WHEN** the newest photo of an album is a video still
- **THEN** the tool sets the thumbnail of the album to `video`
