## ADDED Requirements

### Requirement: Freezing

The assistant SHALL freeze samples.

#### Scenario: Example: a tube is frozen

- **WHEN** ines asks to freeze tube t4
- **AND** the freezer has a free slot
- **THEN** `store_in_freezer` is called once
- **AND** the answer gives the slot

#### Scenario: Example: the freezer is full

- **WHEN** the same request runs while the freezer has no free slot
- **THEN** `store_in_freezer` is never called
- **AND** the answer names the tubes that could be removed

#### Scenario: Example: the tube is taken out again

- **WHEN** the same request runs and ines asks for the tube back afterwards
- **THEN** `store_in_freezer` is called once
- **AND** `take_from_freezer` is called once after it

### Requirement: Freezer records

Every stored tube SHALL be recorded.

#### Scenario: Every stored tube is recorded

- **WHEN** a call of `store_in_freezer` succeeds
- **THEN** the run writes one record that names the slot
