# brewing Specification

## Purpose

Brewers start batches, and the tanks are watched while the beer ferments.

## Requirements

### Requirement: Starting a batch with malt

The system SHALL start a batch when the malt is there.

#### Scenario: Malt in stock

- **WHEN** a brewer starts a batch
- **AND** the malt for the recipe is in stock
- **THEN** the system reserves a tank and prints the brew sheet

### Requirement: Starting a batch without malt

The system SHALL get the malt that a batch needs.

#### Scenario: Malt missing

- **WHEN** a brewer starts a batch
- **AND** the malt for the recipe is not in stock
- **THEN** the system orders the malt from the supplier

### Requirement: Fermentation

The system SHALL watch the temperature of the tanks.

#### Scenario: Tank too warm

- **WHEN** the temperature of a tank rises above 22 degrees
- **THEN** the system opens the cooling valve of the tank
