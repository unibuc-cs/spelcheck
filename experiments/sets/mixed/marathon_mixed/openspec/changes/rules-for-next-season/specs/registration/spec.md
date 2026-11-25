## ADDED Requirements

### Requirement: Charity places

The system SHALL offer places that are sold through a charity.

#### Scenario: Charity place free

- **WHEN** a runner asks for a charity place
- **AND** the charity has places left
- **THEN** the system reserves a charity place for the runner

#### Scenario: Charity full

- **WHEN** a runner asks for a charity place
- **AND** the charity has no places left
- **THEN** the system proposes another charity to the runner

### Requirement: No refunds

The system SHALL keep the fees of runners who withdraw.

#### Scenario: Fee kept

- **WHEN** a runner withdraws from the race
- **THEN** the system keeps the entry fee

### Requirement: Unpaid fees

The system SHALL hold back the bibs of runners who have not paid.

#### Scenario: Fee unpaid

- **WHEN** the entry fee of a runner is unpaid
- **THEN** the system does not hand out any bib

## MODIFIED Requirements

### Requirement: Payment

The system SHALL take the entry fee.

#### Scenario: Payment accepted

- **WHEN** a runner pays the entry fee
- **AND** the payment is accepted
- **THEN** the system sends the runner a receipt

## REMOVED Requirements

### Requirement: Registration when full

**Reason**: The waiting list was never used.

**Migration**: None.

### Requirement: Transfers

**Reason**: Registrations are personal from now on.

**Migration**: None.
