## ADDED Requirements

### Requirement: Standing room

A standing-room ticket SHALL be issued at once.

#### Scenario: Example: a standing ticket

- **WHEN** ravi sends a standing-room request for show s8
- **THEN** the plan is written once
- **AND** `issue_ticket` succeeds once
- **AND** `ask_box_office` is never called
