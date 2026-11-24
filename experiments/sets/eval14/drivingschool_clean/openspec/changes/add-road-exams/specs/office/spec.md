## ADDED Requirements

### Requirement: Road exams

The system SHALL book road exams at the test centre.

#### Scenario: Slot at the test centre

- **WHEN** an instructor asks for a road exam
- **AND** the test centre has a slot
- **THEN** the system books the exam and informs the learner

#### Scenario: No slot

- **WHEN** an instructor asks for a road exam
- **AND** the test centre has no slot
- **THEN** the system puts the learner on the list for the next date
