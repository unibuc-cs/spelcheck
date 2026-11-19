# Requirements: Fleet

## Requirement 1

**User Story:** As an employee, I want to book company cars online, so that I can travel to customers.

### Acceptance Criteria

- F1: WHEN an employee books a car AND a car is free for the requested day, THE Fleet System SHALL reserve the car.
- F2: WHEN an employee books a car AND no car is free for the requested day, THE Fleet System SHALL put the booking on the waiting list.
- F3: WHEN an employee returns a car, THE Fleet System SHALL record the mileage and mark the car as free.
- F4: WHEN the mileage of a car passes its next service limit, THE Fleet System SHALL book the car for a service.
- F5: WHEN an employee reports damage to a car, THE Fleet System SHALL mark the car as unavailable only if a mechanic confirms the damage.
