# Requirements: Gym

## Requirement 1

**User Story:** As a gym member, I want to enter the gym and book classes with my card, so that I can train when I want.

### Acceptance Criteria

- G1: WHEN a member scans the card AND the membership is active, THE Gym System SHALL open the entrance gate.
- G2: WHEN a member scans the card AND the membership has expired, THE Gym System SHALL keep the gate closed and show a renewal message.
- G3: WHEN a member books a class AND the class has free places, THE Gym System SHALL confirm the booking.
- G4: WHEN a member books a class AND the class is full, THE Gym System SHALL put the member on the waiting list.
- G5: WHEN a member cancels a booking at least 2 hours before the class, THE Gym System SHALL give the place to the first member on the waiting list.
- G6: WHEN a member books a class, THE Gym System SHALL NOT put anyone on a waiting list.
