# Requirements: Elevator

## Requirement 1

**User Story:** As a building resident, I want the elevator to answer calls and to move safely, so that I can reach my floor.

### Acceptance Criteria

- E1: WHEN a passenger presses a call button AND the elevator is idle, THE Elevator Controller SHALL close the doors and move the elevator to the calling floor.
- E2: WHEN the door sensor detects an obstruction, THE Elevator Controller SHALL open the doors.
- E3: WHEN a passenger presses the door-open button AND the elevator is stopped at a floor, THE Elevator Controller SHALL open the doors.
- E4: WHEN a passenger presses the alarm button, THE Elevator Controller SHALL connect the cabin to the service line.
- E5: WHEN the doors fail to close for the third time in a row, THE Elevator Controller SHALL take the elevator out of service and notify the maintenance team.
- E6: WHEN the door sensor detects an obstruction, THE Elevator Controller SHALL keep the doors closed.
