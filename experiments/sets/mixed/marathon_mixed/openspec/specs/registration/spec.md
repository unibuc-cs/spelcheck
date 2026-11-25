# registration Specification

## Purpose

Runners register for a city marathon and pay the entry fee.

## Requirements

### Requirement: Registration with places left

The system SHALL register a runner while places are left.

#### Scenario: Places left

- **WHEN** a runner registers
- **AND** places are left
- **THEN** the system confirms the registration and assigns a bib number

### Requirement: Registration when full

The system SHALL keep a waiting list when the race is full.

#### Scenario: No places left

- **WHEN** a runner registers
- **AND** no places are left
- **THEN** the system puts the runner on the waiting list

### Requirement: Medical certificate

The system SHALL check the medical certificate of a runner.

#### Scenario: Certificate valid

- **WHEN** a runner uploads a medical certificate
- **AND** the certificate is valid
- **THEN** the system marks the runner as cleared to start

#### Scenario: Certificate not valid

- **WHEN** a runner uploads a medical certificate
- **AND** the certificate is not valid
- **THEN** the system asks the runner for a new certificate

### Requirement: Payment

The system SHALL take the entry fee.

#### Scenario: Payment accepted

- **WHEN** a runner pays the entry fee
- **AND** the payment is accepted
- **THEN** the system sends the runner a receipt

#### Scenario: Payment not accepted

- **WHEN** a runner pays the entry fee
- **AND** the payment is not accepted
- **THEN** the system asks for another payment method

### Requirement: Withdrawal

The system SHALL let runners withdraw.

#### Scenario: Runner withdraws

- **WHEN** a runner withdraws from the race
- **THEN** the system refunds the entry fee

### Requirement: Payment deadline

The system SHALL act on runners who do not pay in time.

#### Scenario: Second missed deadline

- **WHEN** a runner misses the payment deadline for the second time
- **THEN** the system cancels the registration of the runner

### Requirement: Transfers

The system SHALL let a runner pass the registration on.

#### Scenario: Registration transferred

- **WHEN** a runner transfers the registration to another runner
- **THEN** the system sends the new runner a confirmation

### Requirement: Club discount

The system SHALL give a discount to the members of running clubs.

#### Scenario: Club member

- **WHEN** a runner is a member of a running club
- **THEN** the system applies the club discount to the entry fee
