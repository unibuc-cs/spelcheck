# Requirements: Pool

## Requirement 1

**User Story:** As a swimmer, I want to enter the public pool with my card, so that I do not have to queue at the till.

### Acceptance Criteria

- P1: WHEN a swimmer holds a card at the entry gate AND the card has entries left, THE Pool System SHALL open the gate and deduct one entry.
- P2: WHEN a swimmer holds a card at the entry gate AND the card has no entries left, THE Pool System SHALL keep the gate closed and show where to buy more entries.
- P3: WHEN the water temperature drops below 24 degrees, THE Pool System SHALL alert the pool manager.
- P4: WHEN a swimmer leaves through the exit gate, THE Pool System SHALL record the time of exit.
- P5: WHEN a card is reported lost for the second time, THE Pool System SHALL block the card and charge a replacement fee.
- P6: WHILE the pool is closed for cleaning, THE Pool System SHALL keep the entry gate closed.
