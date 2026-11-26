# Playlists Specification

## Purpose

A service keeps the playlists of its users.

## Requirements

### Requirement: Adding

#### Scenario: Track available

- **WHEN** a user adds a track to a playlist
- **AND** the track is available in the country of the user
- **THEN** the service appends the track to the playlist
- **AND** sets the track state to `playable`

#### Scenario: Track not available

- **WHEN** a user adds a track to a playlist
- **AND** the track is not available in the country of the user
- **THEN** the service appends the track to the playlist
- **AND** sets the track state to `greyed out`

### Requirement: Sharing

#### Scenario: Public playlist

- **WHEN** a user asks for a share link
- **AND** the playlist is public
- **THEN** the service answers with status 200
- **AND** returns the link of the playlist

#### Scenario: Private playlist

- **WHEN** a user asks for a share link
- **AND** the playlist is not public
- **THEN** the service answers with status 403

### Requirement: Deleting

#### Scenario: Playlist deleted

- **WHEN** a user deletes a playlist
- **THEN** the service moves the playlist to the trash

### Requirement: Offline

#### Scenario: Kept on the device

- **WHEN** a playlist is marked for offline use
- **THEN** the service keeps the tracks of the playlist on the device

### Requirement: Cover

#### Scenario: Empty playlist

- **WHEN** a playlist has no tracks
- **THEN** the service sets the cover of the playlist to `blank`

#### Scenario: Album image

- **WHEN** the first track of a playlist has an album image
- **THEN** the service sets the cover of the playlist to `album`

### Requirement: Open links

#### Scenario: Link for everyone

- **WHEN** a user asks for a share link
- **AND** the playlist is not public
- **THEN** the service answers with status 200
