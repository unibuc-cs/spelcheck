# race-day Specification

### Requirement: Heat warning

The system SHALL warn the runners of heat.

#### Scenario N1: Warning in force

- **WHEN** a heat warning is in force
- **THEN** the system shows the warning at the start area and does not open any start gate

### Requirement: Pacers

The system SHALL give runners a pacer for their target time.

#### Scenario N2: Pacer free

- **WHEN** a runner asks for a pacer
- **AND** a pacer for the target time is free
- **THEN** the system assigns the pacer to the runner

# registration Specification

### Requirement: Charity places

The system SHALL offer places that are sold through a charity.

#### Scenario N3: Charity place free

- **WHEN** a runner asks for a charity place
- **AND** the charity has places left
- **THEN** the system reserves a charity place for the runner

#### Scenario N4: Charity full

- **WHEN** a runner asks for a charity place
- **AND** the charity has no places left
- **THEN** the system proposes another charity to the runner

### Requirement: No refunds

The system SHALL keep the fees of runners who withdraw.

#### Scenario N5: Fee kept

- **WHEN** a runner withdraws from the race
- **THEN** the system keeps the entry fee

### Requirement: Unpaid fees

The system SHALL hold back the bibs of runners who have not paid.

#### Scenario N6: Fee unpaid

- **WHEN** the entry fee of a runner is unpaid
- **THEN** the system does not hand out any bib

# results Specification

### Requirement: Certificates

The system SHALL send certificates to runners.

#### Scenario N7: Result final

- **WHEN** a runner asks for a certificate
- **AND** the result of the runner is final
- **THEN** the system sends the certificate by email and adds the split times
