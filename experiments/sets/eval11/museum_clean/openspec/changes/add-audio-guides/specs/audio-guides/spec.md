## Purpose

The museum lends audio guides to visitors for the length of their visit.

## ADDED Requirements

### Requirement: Lending

The system SHALL lend audio guides to visitors.

#### Scenario: Guide in stock

- **WHEN** a visitor asks for an audio guide
- **AND** an audio guide is in stock
- **THEN** the system hands out an audio guide and records the loan

#### Scenario: None in stock

- **WHEN** a visitor asks for an audio guide
- **AND** no audio guide is in stock
- **THEN** the system offers the visitor the guide as a phone app
