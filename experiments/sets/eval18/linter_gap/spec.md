# Linter Specification

## Purpose

A command-line tool, `lnt`, checks the source files of a project.

## Requirements

### Requirement: Check

#### Scenario: Clean files

- **WHEN** the user runs `lnt check`
- **AND** no file has a finding
- **THEN** the tool prints "all files pass"
- **AND** exits with code 0

#### Scenario: Findings

- **WHEN** the user runs `lnt check`
- **AND** a file has a finding
- **THEN** the tool prints each finding with its file and line
- **AND** exits with code 1

### Requirement: Fix

#### Scenario: Automatic fix

- **WHEN** the user runs `lnt fix`
- **AND** the finding has an automatic fix
- **THEN** the tool rewrites the file
- **AND** keeps a copy with the suffix `.orig`

### Requirement: Configuration

#### Scenario: Unknown rule

- **WHEN** the configuration names a rule that does not exist
- **THEN** the tool prints the name of the rule
- **AND** exits with code 2

### Requirement: Cache

#### Scenario: Large cache

- **WHEN** the cache is larger than 500 megabytes
- **THEN** the tool deletes the oldest entries

### Requirement: Ignoring

#### Scenario: File ignored

- **WHEN** the user runs `lnt ignore <file>`
- **THEN** the tool adds the file to `.lntignore`
