## ADDED Requirements

### Requirement: Sibling moves

A pupil SHALL be moved to a sibling's group at once.

#### Scenario: Example: a sibling move

- **WHEN** lena sends a sibling request for pupil p6
- **THEN** the plan is written once
- **AND** `change_group` succeeds once
- **AND** `ask_head_teacher` is never called
