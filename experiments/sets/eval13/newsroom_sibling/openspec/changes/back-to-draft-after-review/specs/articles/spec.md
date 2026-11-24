## MODIFIED Requirements

### Requirement: Review

The system SHALL act on the review of an editor.

#### Scenario: Approved

- **WHEN** an editor reviews an article
- **AND** the article is approved
- **THEN** the system publishes the article on the website

#### Scenario: Not approved

- **WHEN** an editor reviews an article
- **AND** the article is not approved
- **THEN** the system sends the notes of the editor to the reporter and sets the article back to draft
