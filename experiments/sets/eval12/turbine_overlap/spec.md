# Requirements: Turbine

## Requirement 1

**User Story:** As the operator of a wind farm, I want each turbine to protect itself, so that faults and bad weather do no damage.

### Acceptance Criteria

- T1: WHEN an operator sends the start command AND the turbine has no open fault, THE Turbine Controller SHALL release the brake and start the rotor.
- T2: WHEN an operator sends the start command AND the turbine has an open fault, THE Turbine Controller SHALL refuse the command and show the fault.
- T3: WHEN the wind direction changes by more than 10 degrees, THE Turbine Controller SHALL turn the nacelle into the wind.
- T4: WHEN the vibration sensor trips for the third time in a day, THE Turbine Controller SHALL call the maintenance crew.
- T5: WHEN the gearbox oil is hotter than 90 degrees, THE Turbine Controller SHALL lower the power output.
- T6: WHILE ice is detected on the blades, THE Turbine Controller SHALL hold the rotor still.
