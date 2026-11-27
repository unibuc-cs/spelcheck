## ADDED Requirements

### Requirement: Inspection runs

An inspection run SHALL NOT order paint.

#### Scenario: An inspection run orders no paint

- **WHEN** a call of `order_paint` is made
- **THEN** the run is not an inspection run

#### Scenario: An inspection run names the foreman

- **WHEN** a call of `ask_foreman` is made in an inspection run
- **THEN** the answer names the foreman who was asked
