# Requirements: Charging

## Requirement 1

**User Story:** As an electric car driver, I want to charge at public stations with my app, so that I can pay without a card.

### Acceptance Criteria

- C1: WHEN a driver plugs in a car AND the driver's account is active, THE Charging System SHALL start charging.
- C2: WHEN a driver plugs in a car AND the driver's account is suspended, THE Charging System SHALL refuse to charge and show the reason on the display.
- C3: WHEN the battery reaches the charge limit set by the driver, THE Charging System SHALL stop charging.
- C4: WHEN the driver presses stop in the app, THE Charging System SHALL stop charging and unlock the cable.
- C5: WHEN the station loses its network connection for the second time in an hour, THE Charging System SHALL switch to offline mode.
