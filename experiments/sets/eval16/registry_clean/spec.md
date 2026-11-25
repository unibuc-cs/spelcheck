# Registry Specification

## Purpose

A private registry stores the packages of a company and serves them to its build machines.

## Requirements

### Requirement: Publish

#### Scenario: New version

- **WHEN** a maintainer publishes a package version
- **AND** the version does not exist yet
- **THEN** the registry stores the archive
- **AND** adds the version to the package index
- **AND** returns status 201

#### Scenario: Version exists

- **WHEN** a maintainer publishes a package version
- **AND** the version exists already
- **THEN** the registry rejects the upload
- **AND** returns status 409
- **AND** leaves the stored archive unchanged

#### Scenario: Upload too large

- **WHEN** an upload grows beyond 50 megabytes
- **THEN** the registry returns status 413
- **AND** deletes the partial upload

### Requirement: Install

#### Scenario: Version published

- **WHEN** a client requests a package version
- **AND** the version is published
- **THEN** the registry sends the archive
- **AND** increases the download counter

#### Scenario: Version not published

- **WHEN** a client requests a package version
- **AND** the version is not published
- **THEN** the registry returns status 404
- **AND** lists the published versions of the package in the answer

### Requirement: Yank

#### Scenario: Version yanked

- **WHEN** a maintainer yanks a version
- **THEN** the registry marks the version as yanked
- **AND** keeps the archive in storage
- **AND** removes the version from the list of installable versions

#### Scenario: Version restored

- **WHEN** a maintainer restores a yanked version
- **THEN** the registry removes the yanked mark
- **AND** adds the version to the list of installable versions

### Requirement: Tokens

#### Scenario: Token created

- **WHEN** a maintainer creates a token
- **AND** the maintainer has fewer than 10 tokens
- **THEN** the registry issues the token
- **AND** shows the token once

#### Scenario: Token limit

- **WHEN** a maintainer creates a token
- **AND** the maintainer has 10 tokens
- **THEN** the registry refuses with "token limit reached"
- **AND** issues no token

#### Scenario: Unused token

- **WHEN** a token has not been used for 90 days
- **THEN** the registry revokes the token
- **AND** sends a notice to the maintainer

### Requirement: Search

#### Scenario: Matches

- **WHEN** a client searches for a name
- **AND** at least one package matches
- **THEN** the registry returns the matching packages sorted by downloads

#### Scenario: No match

- **WHEN** a client searches for a name
- **AND** no package matches
- **THEN** the registry returns an empty list
- **AND** status 200

### Requirement: Abuse

#### Scenario: Rate limit

- **WHEN** a client sends more than 100 requests in a minute
- **THEN** the registry answers with status 429
- **AND** adds a `Retry-After` header

#### Scenario: Failed sign-ins

- **WHEN** a maintainer fails to sign in for the fifth time in an hour
- **THEN** the registry locks the account of the maintainer for one hour
