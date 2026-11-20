# Requirements: Clinic

## Requirement 1

**User Story:** As a patient, I want to book and manage my appointments online, so that I do not have to phone the clinic.

### Acceptance Criteria

- C1: WHEN a patient requests an appointment AND the doctor has a free slot on the requested day, THE Clinic System SHALL book the slot and send a confirmation.
- C2: WHEN a patient requests an appointment AND the doctor has no free slot on the requested day, THE Clinic System SHALL offer the next free day.
- C3: WHEN a patient cancels an appointment, THE Clinic System SHALL delete the appointment and free the slot.
- C4: WHEN a patient misses an appointment for the second time in a year, THE Clinic System SHALL send the patient a warning letter.
- C5: WHEN a doctor reports sick, THE Clinic System SHALL cancel the doctor's appointments for that day and notify the patients.
- C6: THE Clinic System SHALL keep every appointment in the patient's record for five years.
