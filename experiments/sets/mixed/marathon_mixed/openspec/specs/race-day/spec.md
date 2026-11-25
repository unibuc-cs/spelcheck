# race-day Specification

## Purpose

The start, the course and the finish on the day of the race.

## Requirements

### Requirement: Bib collection

The system SHALL hand out bibs before the race.

#### Scenario: Cleared to start

- **WHEN** a runner collects the bib
- **AND** the runner is cleared to start
- **THEN** the system hands out the bib and the timing chip

#### Scenario: Not cleared to start

- **WHEN** a runner collects the bib
- **AND** the runner is not cleared to start
- **THEN** the system sends the runner to the medical desk

### Requirement: Start waves

The system SHALL start the runners in waves.

#### Scenario: Runner in the wave

- **WHEN** a start wave is called
- **AND** the runner belongs to the wave
- **THEN** the system opens the start gate for the runner

#### Scenario: Runner in another wave

- **WHEN** a start wave is called
- **AND** the runner does not belong to the wave
- **THEN** the system shows the runner the right wave

### Requirement: Checkpoints

The system SHALL time the runners on the course.

#### Scenario: Checkpoint passed

- **WHEN** a runner passes a checkpoint
- **THEN** the system records the split time of the runner

### Requirement: Cut-off

The system SHALL close the checkpoints in time.

#### Scenario: Cut-off time passed

- **WHEN** the cut-off time of a checkpoint has passed
- **THEN** the system closes the checkpoint

### Requirement: Heat warning

The system SHALL warn the runners of heat.

#### Scenario: Warning in force

- **WHEN** a heat warning is in force
- **THEN** the system shows the warning at the start area

### Requirement: Drop-outs

The system SHALL look after runners who drop out.

#### Scenario: Runner injured

- **WHEN** a runner drops out
- **AND** the runner is injured
- **THEN** the system calls the medical team

#### Scenario: Runner not injured

- **WHEN** a runner drops out
- **AND** the runner is not injured
- **THEN** the system sends the sweep bus

### Requirement: Lost chips

The system SHALL act on lost timing chips.

#### Scenario: Second lost chip

- **WHEN** a runner loses a timing chip for the second time
- **THEN** the system charges the runner for the chip
