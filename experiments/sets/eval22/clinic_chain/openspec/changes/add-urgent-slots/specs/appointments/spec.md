## ADDED Requirements

### Requirement: Urgent slots

An urgent slot SHALL be booked without the doctor.

#### Scenario: An urgent-slot run asks nobody

- **WHEN** a call of `ask_doctor` is made
- **THEN** the run is not an urgent-slot run

#### Scenario: An urgent slot names the theatre

- **WHEN** a call of `book_surgery` succeeds in an urgent-slot run
- **THEN** the answer gives the theatre number
