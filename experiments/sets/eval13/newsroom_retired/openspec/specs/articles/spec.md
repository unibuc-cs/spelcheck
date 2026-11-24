# articles Specification

## Purpose

Reporters hand in articles, and editors review and publish them.

## Requirements

### Requirement: Articles with sources

The system SHALL pass on articles that name their sources.

#### Scenario: Source list attached

- **WHEN** a reporter submits an article
- **AND** the article has a source list
- **THEN** the system sends the article to the editor on duty

### Requirement: Articles without sources

The system SHALL send back articles that name no sources.

#### Scenario: No source list

- **WHEN** a reporter submits an article
- **AND** the article has no source list
- **THEN** the system returns the article to the reporter

### Requirement: Review

The system SHALL act on the review of an editor.

#### Scenario: Approved

- **WHEN** an editor reviews an article
- **AND** the article is approved
- **THEN** the system publishes the article on the website

#### Scenario: Not approved

- **WHEN** an editor reviews an article
- **AND** the article is not approved
- **THEN** the system sends the notes of the editor to the reporter
