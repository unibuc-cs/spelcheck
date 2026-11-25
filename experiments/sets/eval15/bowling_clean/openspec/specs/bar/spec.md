# bar Specification

## Purpose

Shoes, fouls, the league, and notices.

## Requirements

### Requirement: Shoe hire

The system SHALL hire out shoes.

#### Scenario: Shoes in stock

- **WHEN** a player asks for shoes
- **AND** shoes of the size are in stock
- **THEN** the system hands out a pair of shoes

#### Scenario: Shoes out of stock

- **WHEN** a player asks for shoes
- **AND** shoes of the size are not in stock
- **THEN** the system offers the player shoe covers

### Requirement: Fouls

The system SHALL act on fouls.

#### Scenario: Third foul

- **WHEN** a player steps over the foul line for the third time in a game
- **THEN** the system ends the game of the player

### Requirement: League nights

The system SHALL announce league nights.

#### Scenario: League night

- **WHEN** a league match is being played
- **THEN** the system shows the league table above the bar
