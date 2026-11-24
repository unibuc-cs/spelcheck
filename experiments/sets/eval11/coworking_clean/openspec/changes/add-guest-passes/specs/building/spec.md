## ADDED Requirements

### Requirement: Guests

The system SHALL register guests at the reception.

#### Scenario: Host present

- **WHEN** a guest arrives at the reception
- **AND** the host is in the building
- **THEN** the system prints a guest pass and informs the host

#### Scenario: Host absent

- **WHEN** a guest arrives at the reception
- **AND** the host is not in the building
- **THEN** the system asks the guest to wait and calls the host

## REMOVED Requirements

### Requirement: Printer

**Reason**: The printer is replaced by a leased one that the supplier monitors.

**Migration**: None. The supplier's own service takes over.
