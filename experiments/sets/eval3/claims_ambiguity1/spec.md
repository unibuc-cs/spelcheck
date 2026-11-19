# Claims Specification

## Purpose

Policy holders file insurance claims online; small claims are paid automatically.

## Requirements

### Requirement: Filing

#### Scenario: Covered damage

- **WHEN** a policy holder files a claim
- **AND** the damage is covered by the policy
- **THEN** the system registers the claim

#### Scenario: Damage not covered

- **WHEN** a policy holder files a claim
- **AND** the damage is not covered by the policy
- **THEN** the system rejects the claim and explains why

### Requirement: Payment

#### Scenario: Small claim

- **WHEN** a registered claim is below 1000 euros
- **THEN** the system pays the claim automatically and sends a receipt if the claim matches no fraud pattern

#### Scenario: Large claim

- **WHEN** a registered claim is 1000 euros or more
- **AND** it matches no fraud pattern
- **THEN** the system assigns the claim to an assessor

### Requirement: Fraud

#### Scenario: Fraud suspicion

- **WHEN** a claim matches a fraud pattern
- **THEN** the system assigns the claim to the fraud team
