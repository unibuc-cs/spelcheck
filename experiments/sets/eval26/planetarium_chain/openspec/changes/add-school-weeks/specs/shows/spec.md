## ADDED Requirements

### Requirement: School weeks

In a school week the dome SHALL be booked without the astronomer.

#### Scenario: A school-week run asks nobody

- **WHEN** a call of `ask_astronomer` is made
- **THEN** the run is not a school-week run

#### Scenario: A school-week booking names the guide

- **WHEN** a call of `book_dome` succeeds in a school-week run
- **THEN** the answer names the guide
