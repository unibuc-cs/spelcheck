## ADDED Requirements

### Requirement: Shipping runs

A shipping run SHALL NOT grade fruit.

#### Scenario: A shipping run grades no fruit

- **WHEN** a call of `grade_fruit` is made
- **THEN** the run is not a shipping run

#### Scenario: A shipping run gives the weight

- **WHEN** a call of `ship_crates` succeeds in a shipping run
- **THEN** the answer gives the total weight
