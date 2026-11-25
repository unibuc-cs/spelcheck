# Thumbs Specification

## Purpose

A service stores uploaded images and renders thumbnails of them on request.

## Requirements

### Requirement: Upload

#### Scenario: Supported format

- **WHEN** a client uploads an image
- **AND** the format is supported
- **THEN** the service stores the original
- **AND** returns the id of the image
- **AND** queues the standard sizes for rendering

#### Scenario: Unsupported format

- **WHEN** a client uploads an image
- **AND** the format is not supported
- **THEN** the service returns status 415
- **AND** names the supported formats in the answer
- **AND** stores nothing

#### Scenario: Metadata

- **WHEN** a client asks for the metadata of an image
- **THEN** the service returns the width
- **AND** the height
- **AND** the format of the original

### Requirement: Rendering

#### Scenario: Cached size

- **WHEN** a thumbnail is requested
- **AND** the size was rendered before
- **THEN** the service sends the cached thumbnail
- **AND** sets the `X-Cache` header to `hit`

#### Scenario: New size

- **WHEN** a thumbnail is requested
- **AND** the size was not rendered before
- **THEN** the service renders the thumbnail
- **AND** stores it in the cache
- **AND** sets the `X-Cache` header to `miss`

#### Scenario: Slow rendering

- **WHEN** rendering a thumbnail takes longer than 5 seconds
- **THEN** the service cancels the rendering
- **AND** returns status 504

### Requirement: Purge

#### Scenario: No legal hold

- **WHEN** an owner deletes an image
- **AND** the image has no legal hold
- **THEN** the service deletes the original
- **AND** deletes every cached thumbnail
- **AND** returns status 204

#### Scenario: Legal hold

- **WHEN** an owner deletes an image
- **AND** the image has a legal hold
- **THEN** the service refuses with status 423
- **AND** keeps the original

### Requirement: Cache

#### Scenario: Disk pressure

- **WHEN** the cache grows beyond 80 percent of its disk
- **THEN** the service evicts the thumbnails that were not requested for the longest time

#### Scenario: Cache cleared

- **WHEN** the operator runs `thumbs cache clear`
- **THEN** the service deletes every cached thumbnail
- **AND** prints the number of files deleted

### Requirement: Usage

#### Scenario: Paid plan

- **WHEN** an account asks for its usage
- **AND** the account has a paid plan
- **THEN** the service returns the bytes stored
- **AND** the bytes left in the quota

#### Scenario: No paid plan

- **WHEN** an account asks for its usage
- **AND** the account has no paid plan
- **THEN** the service returns the bytes stored
- **AND** a link to the plans

### Requirement: Watermarks

#### Scenario: Watermark option

- **WHEN** an account switches the `watermark` option on
- **THEN** the service asks for the watermark image
- **AND** shows a preview

### Requirement: Abuse

#### Scenario: Unknown images

- **WHEN** a client requests a thumbnail of an unknown image for the twentieth time in a minute
- **THEN** the service blocks the address of the client for ten minutes

### Requirement: Freshness

#### Scenario: Always render

- **WHEN** a thumbnail is requested
- **AND** the size was rendered before
- **THEN** the service renders the thumbnail again
- **AND** sets the `X-Cache` header to `miss`
