# Requirements: Hotel

## Requirement 1

**User Story:** As a hotel guest, I want to check in at a kiosk and open my room with a key card, so that I do not have to wait at the desk.

### Acceptance Criteria

- H1: WHEN a guest scans a booking code at the kiosk AND the room is ready, THE Hotel System SHALL issue a key card for the room.
- H2: WHEN a guest scans a booking code at the kiosk AND the room is not ready, THE Hotel System SHALL show the time at which the room will be ready.
- H3: WHEN a key card is held to a door lock AND the card is valid for the room, THE Hotel System SHALL unlock the door.
- H4: WHEN a key card is rejected by a door lock for the third time in a row, THE Hotel System SHALL alert the front desk.
- H5: WHEN a guest checks out, THE Hotel System SHALL deactivate the guest's key cards and send the bill by email if the guest asked for it.
