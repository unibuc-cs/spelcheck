# Requirements: Meters

## Requirement 1

**User Story:** As a household customer, I want my electricity use read and billed automatically, so that I do not have to send readings.

### Acceptance Criteria

- M1: WHEN a meter sends a reading AND the reading is not lower than the previous one, THE Metering System SHALL store the reading.
- M2: WHEN a billing period ends, THE Metering System SHALL create a bill from the stored readings.
- M3: WHEN a bill has been unpaid for more than 30 days, THE Metering System SHALL send a reminder to the customer.
- M4: WHEN a meter fails to send a reading for the third time in a row, THE Metering System SHALL send a technician.
