# Requirements: Beds

## Requirement 1

**User Story:** As a ward nurse, I want beds assigned to arriving patients, so that nobody waits in the corridor.

### Acceptance Criteria

- B1: WHEN a patient arrives on the ward AND a bed is free, THE Bed System SHALL assign a bed to the patient and inform the nurse.
- B2: WHEN a patient is discharged, THE Bed System SHALL release the patient's bed and mark it for cleaning.
- B3: WHEN a bed is reported broken for the second time in a month, THE Bed System SHALL order a replacement.
- B4: WHEN a bed has been marked for cleaning for more than 2 hours, THE Bed System SHALL alert the cleaning team.
