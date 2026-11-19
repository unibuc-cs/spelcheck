# Requirements: Printing

## Requirement 1

**User Story:** As an office worker, I want my print jobs handled reliably, so that I get my pages quickly.

### Acceptance Criteria

- P1: WHEN a user sends a print job AND the printer is ready, THE Print Server SHALL add the job to the queue.
- P2: WHEN a user sends a print job AND the printer is offline, THE Print Server SHALL hold the job and notify the user.
- P3: WHEN a user sends a print job of more than 100 pages, THE Print Server SHALL show the user a warning about paper use.
- P4: WHEN the printer runs out of paper, THE Print Server SHALL pause the queue and alert the office manager.
- P5: WHEN the printer has jammed three times in one day, THE Print Server SHALL take the printer offline and call the service technician.
