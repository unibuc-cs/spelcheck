# Requirements: Crossing

## Requirement 1

**User Story:** As a road user, I want the level crossing to close while a train passes, so that I can cross the railway safely.

### Acceptance Criteria

- C1: WHEN a train approaches the crossing AND the barriers are working, THE Crossing System SHALL lower the barriers and switch on the warning lights.
- C2: WHEN a train approaches the crossing AND the barriers are not working, THE Crossing System SHALL tell the train driver to stop before the crossing.
- C3: WHEN a train has passed the crossing, THE Crossing System SHALL raise the barriers and switch off the warning lights.
- C4: WHEN a barrier fails to lower for the third time in a week, THE Crossing System SHALL report the crossing to maintenance.
- C5: WHEN a vehicle has stood on the crossing for more than 20 seconds, THE Crossing System SHALL warn the signal box.
- C6: WHEN a train has passed the crossing, THE Crossing System SHALL keep the barriers down.
