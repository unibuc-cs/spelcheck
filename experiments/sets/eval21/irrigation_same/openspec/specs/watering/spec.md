# watering Specification

## Purpose

A farm assistant handles the requests of growers and calls the tools of the irrigation system.

## Requirements

### Requirement: Soil check before watering

A field SHALL NOT be watered without a soil check.

#### Scenario: No watering without a soil check

- **WHEN** a call of `open_valve` succeeds
- **THEN** an earlier call of `check_soil` in the run succeeded

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: a field is watered

- **WHEN** iris asks to water field f3
- **THEN** `open_valve` is called once
- **AND** the answer gives the minutes

### Requirement: Weather

Reading the weather SHALL change nothing.

#### Scenario: Reading the weather changes nothing

- **WHEN** a call of `read_weather` succeeds
- **THEN** no valve changes in that call
