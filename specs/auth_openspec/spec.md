# auth Specification

## Purpose

Password login with account lockout. Written in the OpenSpec format
(`### Requirement` / `#### Scenario`) to show that speccheck does not depend on
the EARS wording used by Kiro.

## Requirements

### Requirement: Login

The system SHALL authenticate users by password.

#### Scenario: Valid credentials

- **WHEN** a user submits a correct password
- **THEN** the system grants access

#### Scenario: Invalid credentials

- **WHEN** a user submits an incorrect password
- **THEN** the system denies access

### Requirement: Account Lockout

The system SHALL lock an account after repeated failed attempts.

#### Scenario: Lockout threshold

- **WHEN** the number of failed attempts on an account reaches 5
- **THEN** the system locks the account

#### Scenario: Locked account

- **WHEN** a user submits a password for a locked account
- **THEN** the system denies access

### Requirement: Administrator Access

Administrators must always be able to reach the system.

#### Scenario: Administrators are never locked out

- **WHEN** the account belongs to an administrator
- **THEN** the system does not lock the account
