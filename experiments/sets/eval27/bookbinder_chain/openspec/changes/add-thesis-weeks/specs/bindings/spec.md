## ADDED Requirements

### Requirement: Thesis weeks

In a thesis week a binding SHALL be started without the master.

#### Scenario: A thesis-week run asks nobody

- **WHEN** a call of `ask_master` is made
- **THEN** the run is not a thesis-week run

#### Scenario: A thesis binding names the cover

- **WHEN** a call of `start_binding` succeeds in a thesis-week run
- **THEN** the answer names the cover colour
