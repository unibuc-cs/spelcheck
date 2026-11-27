## ADDED Requirements

### Requirement: Same-day moves

A same-day move SHALL be started without the dispatcher.

#### Scenario: A same-day run asks nobody

- **WHEN** a call of `ask_dispatcher` is made
- **THEN** the run is not a same-day run

#### Scenario: A same-day move names the crew

- **WHEN** a call of `send_truck` succeeds in a same-day run
- **THEN** the answer gives the crew's phone number
