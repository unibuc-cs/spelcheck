# Pager Specification

## Purpose

A service calls the engineers on duty when an alert comes in.

## Requirements

### Requirement: Paging

#### Scenario: Engineer on duty

- **WHEN** an alert comes in
- **AND** an engineer is on duty
- **THEN** the service pages the engineer
- **AND** sets the alert state to `paged`

#### Scenario: Nobody on duty

- **WHEN** an alert comes in
- **AND** no engineer is on duty
- **THEN** the service pages the team lead
- **AND** sets the alert state to `escalated`

### Requirement: Acknowledging

#### Scenario: Alert acknowledged

- **WHEN** an engineer acknowledges an alert
- **THEN** the service sets the alert state to `acknowledged`
- **AND** stops the reminders

### Requirement: Reminders

#### Scenario: No answer

- **WHEN** the time without an acknowledgement of a page reaches 15 minutes
- **THEN** the service pages the next engineer in the rota

### Requirement: Resolving

#### Scenario: Alert resolved

- **WHEN** an engineer resolves an alert
- **THEN** the service sets the alert state to `resolved`
- **AND** writes the duration to the report

### Requirement: Rota

#### Scenario: Swap accepted

- **WHEN** an engineer asks for a swap
- **AND** the other engineer accepts
- **THEN** the service exchanges the two shifts in the rota

#### Scenario: Swap not accepted

- **WHEN** an engineer asks for a swap
- **AND** the other engineer does not accept
- **THEN** the service keeps the rota
- **AND** informs the engineer
