# Requirements: Pharmacy

## Requirement 1

**User Story:** As a patient, I want to refill my prescriptions online, so that I do not run out of medicine.

### Acceptance Criteria

- P1: WHEN a patient requests a refill AND the prescription has refills left AND the prescription has not expired, THE Pharmacy System SHALL prepare the refill.
- P2: WHEN a patient requests a refill AND the prescription has no refills left, THE Pharmacy System SHALL send a renewal request to the doctor.
- P3: WHEN a patient requests a refill AND the prescription has expired, THE Pharmacy System SHALL reject the request.
- P4: WHEN a refill is prepared, THE Pharmacy System SHALL notify the patient that it is ready for pickup.
- P5: WHEN a refill has not been picked up after 10 days, THE Pharmacy System SHALL put the medicine back into stock.
