# Requirements: Irrigation

## Requirement 1

**User Story:** As a gardener, I want the garden watered automatically, so that the plants get enough water without waste.

### Acceptance Criteria

- I1: WHEN the schedule starts a watering cycle AND the soil is dry AND no rain is forecast, THE Irrigation Controller SHALL open the water valve.
- I2: WHEN the schedule starts a watering cycle AND rain is forecast, THE Irrigation Controller SHALL keep the water valve closed and log the skipped cycle.
- I3: WHEN the flow sensor reports a leak, THE Irrigation Controller SHALL close the water valve and alert the gardener if notifications are switched on.
- I4: WHEN the gardener presses the pause button, THE Irrigation Controller SHALL suspend the schedule for 24 hours.
- I5: WHEN the soil sensor fails to answer for the third time in a row, THE Irrigation Controller SHALL switch to the fixed backup schedule.
