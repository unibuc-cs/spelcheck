## ADDED Requirements

### Requirement: Watering by hand

Young plants SHALL be watered by hand.

#### Scenario: Example: watering by hand only

- **WHEN** iris asks to water field f3
- **THEN** `open_valve` is never called
- **AND** the answer tells iris to water by hand
