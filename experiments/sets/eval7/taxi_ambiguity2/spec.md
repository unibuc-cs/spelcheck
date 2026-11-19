# Requirements: Taxi

## Requirement 1

**User Story:** As a passenger, I want to order a taxi from my phone, so that I get a ride quickly.

### Acceptance Criteria

- T1: WHEN a passenger requests a ride AND a driver is nearby, THE Taxi System SHALL assign the nearest driver.
- T2: WHEN a passenger requests a ride AND no driver is nearby, THE Taxi System SHALL tell the passenger the expected waiting time.
- T3: WHEN a driver accepts a ride, THE Taxi System SHALL send the driver's position to the passenger.
- T4: WHEN a passenger cancels a ride after the driver has arrived or after five minutes and the passenger is not a premium member, THE Taxi System SHALL charge a cancellation fee.
- T5: WHEN a ride ends, THE Taxi System SHALL charge the fare and ask the passenger for a rating.
