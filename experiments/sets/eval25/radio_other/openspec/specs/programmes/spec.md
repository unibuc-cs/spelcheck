# programmes Specification

## Purpose

A planning assistant handles the requests of a local radio station and calls the tools of the schedule system.

## Requirements

### Requirement: Jingles

The news SHALL be announced by a jingle.

#### Scenario: The news has a jingle

- **WHEN** a call of `schedule_news` succeeds
- **THEN** a jingle is played before the news

### Requirement: Listener requests

A listener request SHALL change no programme.

#### Scenario: A listener request changes nothing

- **WHEN** a listener request is handled in a run
- **THEN** no programme is changed in the run

### Requirement: Weekly check

The weekly check SHALL report every problem.

#### Scenario: The weekly check reports everything

- **WHEN** a weekly check is handled in a run
- **THEN** every problem of every programme on air is reported in the answer

### Requirement: Requests

The assistant SHALL handle the requests below as described.

#### Scenario: Example: the news is scheduled

- **WHEN** ada asks to schedule the news at noon
- **THEN** `schedule_news` is called once
- **AND** the answer gives the studio
