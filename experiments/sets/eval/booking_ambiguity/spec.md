# Requirements: Booking

## Requirement 1

**User Story:** As a patient, I want to book and cancel appointments online, so that I do not have to call the practice.

### Acceptance Criteria

- B1: WHEN a patient requests an appointment AND the time slot is free, THE Booking System SHALL confirm the appointment.
- B2: WHEN a patient requests an appointment AND the time slot is taken, THE Booking System SHALL offer the next free time slot.
- B3: WHEN a patient cancels an appointment at least 24 hours before its start, THE Booking System SHALL cancel the appointment without a fee.
- B4: WHEN a patient cancels an appointment within 24 hours of its start, THE Booking System SHALL cancel the appointment and charge a late fee.
- B5: WHEN an appointment is confirmed, THE Booking System SHALL send a confirmation message to the patient.
