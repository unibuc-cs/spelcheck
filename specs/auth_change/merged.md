# auth Specification

## Purpose

Password login with account lockout: what the system does today. The change
in `openspec/changes/admin-never-locked` is checked against it.

## Requirements

### Requirement: Login

The system SHALL authenticate users by password.

#### Scenario R1: Valid credentials

- **WHEN** a user submits a correct password
- **THEN** the system grants access

#### Scenario R2: Invalid credentials

- **WHEN** a user submits an incorrect password
- **THEN** the system denies access

### Requirement: Account Lockout

The system SHALL lock an account after repeated failed attempts.

#### Scenario R3: Lockout threshold

- **WHEN** the number of failed attempts on an account reaches 5
- **THEN** the system locks the account

#### Scenario R4: Locked account

- **WHEN** a user submits a password for a locked account
- **THEN** the system denies access

### Requirement: Administrator Access

Administrators MUST always be able to reach the system.

#### Scenario R5: Administrators are never locked out

- **WHEN** the account belongs to an administrator
- **THEN** the system does not lock the account
