# Dns Specification

## Purpose

A service manages the DNS records of the domains of its customers.

## Requirements

### Requirement: Records

#### Scenario: Valid record

- **WHEN** a customer adds a record
- **AND** the record is valid
- **THEN** the service stores the record
- **AND** sets the zone state to `pending-sync`

#### Scenario: Invalid record

- **WHEN** a customer adds a record
- **AND** the record is not valid
- **THEN** the service answers with status 400
- **AND** names the field that is wrong

### Requirement: Sync

#### Scenario: Name servers reachable

- **WHEN** a zone is synced
- **AND** the name servers are reachable
- **THEN** the service sets the zone state to `in-sync`
- **AND** writes the serial number to the log

#### Scenario: Name servers not reachable

- **WHEN** a zone is synced
- **AND** the name servers are not reachable
- **THEN** the service sets the zone state to `sync-failed`
- **AND** tries again after 60 seconds

### Requirement: Lookup

#### Scenario: Name exists

- **WHEN** a client looks up a name
- **AND** the name exists in the zone
- **THEN** the service answers with the record
- **AND** the code `NOERROR`

#### Scenario: Name missing

- **WHEN** a client looks up a name
- **AND** the name does not exist in the zone
- **THEN** the service answers with the code `NXDOMAIN`

### Requirement: Transfer

#### Scenario: Code accepted

- **WHEN** a customer transfers a domain
- **AND** the transfer code is correct
- **THEN** the service starts the transfer
- **AND** sets the domain state to `transfer-out`

#### Scenario: Code refused

- **WHEN** a customer transfers a domain
- **AND** the transfer code is not correct
- **THEN** the service answers with status 403

### Requirement: Expiry

#### Scenario: Domain expires

- **WHEN** a domain passes its expiry date
- **THEN** the service sends a reminder to the customer

### Requirement: Abuse

#### Scenario: Fifth wrong code

- **WHEN** a wrong transfer code is entered for the fifth time for a domain
- **THEN** the service writes the address of the customer to the abuse log

### Requirement: Optimistic sync

#### Scenario: Assume success

- **WHEN** a zone is synced
- **AND** the name servers are not reachable
- **THEN** the service sets the zone state to `in-sync`
