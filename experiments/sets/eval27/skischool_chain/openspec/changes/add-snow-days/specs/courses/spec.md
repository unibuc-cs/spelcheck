## ADDED Requirements

### Requirement: Snow days

On a snow day a pupil SHALL be moved without the head instructor.

#### Scenario: A snow-day run asks nobody

- **WHEN** a call of `ask_head_instructor` is made
- **THEN** the run is not a snow-day run

#### Scenario: A snow-day move names the slope

- **WHEN** a call of `move_pupil` succeeds in a snow-day run
- **THEN** the answer names the slope
