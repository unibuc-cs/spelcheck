## ADDED Requirements

### Requirement: Emergencies

An emergency extraction SHALL be booked without the dentist's approval.

#### Scenario: An emergency run asks nobody

- **WHEN** a call of `ask_dentist` is made
- **THEN** the run is not an emergency run

#### Scenario: An emergency gets the first chair

- **WHEN** a call of `book_extraction` succeeds in an emergency run
- **THEN** the answer gives the first free chair
