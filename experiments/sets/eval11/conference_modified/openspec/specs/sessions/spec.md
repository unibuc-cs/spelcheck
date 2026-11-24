# sessions Specification

## Purpose

The talks, their speakers and the questions of the audience.

## Requirements

### Requirement: Questions

The system SHALL collect questions for the speakers.

#### Scenario: Question sent

- **WHEN** a participant sends a question during a talk
- **THEN** the system shows the question to the moderator

### Requirement: Slides

The system SHALL watch the deadline for the slides.

#### Scenario: Second missed deadline

- **WHEN** a speaker misses the deadline for the slides for the second time
- **THEN** the system informs the programme chair
