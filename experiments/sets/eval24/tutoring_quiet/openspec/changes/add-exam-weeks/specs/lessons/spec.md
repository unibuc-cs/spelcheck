## ADDED Requirements

### Requirement: Exam weeks

An exam-week run SHALL NOT swap rooms.

#### Scenario: An exam-week run swaps no room

- **WHEN** a call of `swap_room` is made
- **THEN** the run is not an exam-week run

#### Scenario: An exam-week run names the head teacher

- **WHEN** a call of `ask_head_teacher` is made in an exam-week run
- **THEN** the answer names the head teacher who was asked
