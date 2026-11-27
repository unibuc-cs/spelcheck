## ADDED Requirements

### Requirement: Empty units

The lock of an empty unit SHALL be changed without a notice.

#### Scenario: An empty-unit run sends no notice for a lock

- **WHEN** a call of `change_lock` is made in an empty-unit run
- **THEN** the run sends no notice to the tenant

#### Scenario: An empty unit gets a new key number

- **WHEN** a call of `change_lock` succeeds in an empty-unit run
- **THEN** the answer gives the new key number
