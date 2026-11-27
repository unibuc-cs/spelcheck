## ADDED Requirements

### Requirement: Last-minute tickets

A last-minute ticket SHALL be issued without the box office.

#### Scenario: A last-minute run asks nobody

- **WHEN** a call of `ask_box_office` is made
- **THEN** the run is not a last-minute run

#### Scenario: A last-minute ticket names the gate

- **WHEN** a call of `issue_ticket` succeeds in a last-minute run
- **THEN** the answer gives the gate number
