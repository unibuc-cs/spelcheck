## ADDED Requirements

### Requirement: Price mails

A price list SHALL be mailed on request.

#### Scenario: A price request is mailed

- **WHEN** a price request is handled in a run
- **THEN** `send_mail` is called once in the run
