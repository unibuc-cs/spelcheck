# Requirements: Thermostat

## Requirement 1

**User Story:** As a resident, I want the heating to keep my home comfortable without wasting energy.

### Acceptance Criteria

- T1: WHEN the room temperature is below 19 degrees AND the heating mode is on AND no window is open, THE Thermostat SHALL turn the boiler on.
- T2: WHEN the room temperature is above 22 degrees, THE Thermostat SHALL turn the boiler off.
- T3: WHILE a window is open, THE Thermostat SHALL turn the boiler off.
- T4: WHILE the heating mode is off, THE Thermostat SHALL turn the boiler off.
- T5: WHEN the boiler reports a fault, THE Thermostat SHALL display a warning.
- T6: WHEN the room temperature is below 19 degrees AND the heating mode is on AND no window is open, THE Thermostat SHALL keep the boiler off to save energy.
